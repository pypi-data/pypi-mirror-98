import logging

from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods

from dj_smail.forms import CertificateForm, CertificateWithKeyForm, CaCertificateForm
from dj_smail.forms import CertificateWithKeyImportForm, CertificateImportForm, CaCertificateImportForm
from dj_smail.models import CaCertificate, Certificate, CertificateWithKey

log = logging.getLogger(__name__)


class BaseCertificateAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('dj_smail/css/admin-extra.css',)
        }

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if obj:
            add_fieldsets = (
                ('Certificate', {
                    'fields': ('certificate_txt',)
                }),
                ('Certificate Issuer Info', {
                    'fields': ('issuer',),
                    'description': '<strong>This is</strong> some <i>explanation</i> about Issuer Info'
                }),
                ('Certificate Info', {
                    'fields': ('serial_number', 'serial_hex', 'subject', 'cn',
                               'is_root_ca', 'is_intermediate_ca', 'is_end_entity',
                               'san_email', 'fingerprint_sha256'),
                }),
                ('Certificate Dates', {
                    'fields': ('not_valid_before', 'not_valid_after'),
                    # 'classes': ['collapse']
                }),
            )

            fieldsets = list(add_fieldsets)  # overwrite fieldset

        return fieldsets

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)

        # unless object is being created: render pem fields as "disabled"
        fields_to_disable_on_edit = ['certificate_txt']
        for field_name in fields_to_disable_on_edit:
            if obj:
                form.base_fields[field_name].disabled = True
            else:
                form.base_fields[field_name].disabled = False

        return form

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))

        if obj:  # This is the case when obj is already created i.e. it's an edit
            readonly_fields.extend([
                'serial_number',
                'serial_hex',
                'subject',
                'cn',
                'issuer',
                'is_self_signed',
                'is_root_ca',
                'is_intermediate_ca',
                'is_end_entity',
                'not_valid_before',
                'not_valid_after',
                'san_email',
                'fingerprint_sha256'
            ])

        return readonly_fields

    def is_self_signed(self, obj):
        return obj.is_self_signed

    is_self_signed.boolean = True

    def is_root_ca(self, obj):
        return obj.is_root_ca

    is_root_ca.boolean = True

    def is_intermediate_ca(self, obj):
        return obj.is_intermediate_ca

    is_intermediate_ca.boolean = True

    def is_end_entity(self, obj):
        return obj.is_end_entity

    is_end_entity.boolean = True


class CertificateAdmin(BaseCertificateAdmin):
    form = CertificateForm
    import_form = CertificateImportForm

    def get_urls(self):
        urls = super().get_urls()
        urls = [x for x in urls if not x.pattern == 'import_certificate/']

        my_urls = [
            path('import_certificate/',
                 self.admin_site.admin_view(self.import_certificate),
                 name='import_certificate')
        ]
        return my_urls + urls

    def import_certificate(self, request):

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            original="Import Certificate",
            opts=self.opts,
            change=True,
            is_popup=False,
            save_as=False,
            has_view_permission=True,
            has_delete_permission=False,
            has_add_permission=False,
            has_change_permission=False
        )

        if request.method == 'POST':
            form = self.import_form(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                # ToDo(frennkie) could also add link to change site of new object
                self.message_user(request, "Successfully imported: %s" % form.instance)
        else:
            form = self.import_form()

        context.update({'form': form})

        template = 'admin/{}/{}/{}'.format(self.opts.app_label,
                                           self.opts.model_name,
                                           'import_certificate.html')
        return TemplateResponse(request, template, context)


class CaCertificateAdmin(CertificateAdmin):
    form = CaCertificateForm
    import_form = CaCertificateImportForm

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path('import_certificate/',
                 self.admin_site.admin_view(self.import_certificate),
                 name='import_cacertificate')
        ]
        return my_urls + urls


class CertificateWithKeyAdmin(BaseCertificateAdmin):
    form = CertificateWithKeyForm
    import_form = CertificateWithKeyImportForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if obj:
            if obj.is_private_key_encrypted:
                if obj.is_secret_key_unchanged:
                    fieldset_private_key = 'Private Key', {
                        'fields': ('private_key_txt',
                                   'is_private_key_encrypted',
                                   'passphrase')
                    }
                else:
                    fieldset_private_key = ('Private Key', {
                        'fields': ('private_key_txt',
                                   'is_private_key_encrypted',
                                   'passphrase',
                                   'private_key_passphrase')
                    })
            else:
                fieldset_private_key = ('Private Key', {
                    'fields': ('private_key_txt',
                               'is_private_key_encrypted')
                })

            fieldset_ca_certs = ('Root CA and Intermediate Certificates', {
                'fields': ('ca_certs',)
            })

            add_fieldsets = (fieldset_private_key, fieldset_ca_certs,)

            fieldsets = fieldsets + list(add_fieldsets)

        return fieldsets

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)

        if obj:
            # unless object is being created: render pem fields as "disabled"
            fields_to_disable_on_edit = ['certificate_txt', 'private_key_txt']
            for field_name in fields_to_disable_on_edit:
                form.base_fields[field_name].disabled = True

            # unless object is being created: remove cleartext passphrase field
            if obj.is_private_key_encrypted:
                if not obj.is_secret_key_unchanged:
                    form.base_fields['private_key_passphrase'].help_text = _(
                        "The SECRET_KEY of the application has changed. The Private Key is "
                        "no longer usable. Please re-enter the Passphrase.")

        return form

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))

        if obj:  # This is the case when obj is already created i.e. it's an edit
            readonly_fields.extend(['is_private_key_encrypted',
                                    'passphrase',
                                    'ca_certs'])

            if not obj.is_secret_key_unchanged:
                readonly_fields.insert(0, 'is_secret_key_unchanged')

        return readonly_fields

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path('import_certificate/',
                 self.admin_site.admin_view(self.import_certificate_with_key),
                 name='import_certificate_with_key')
        ]
        return my_urls + urls

    @method_decorator(require_http_methods(["GET", "POST"]))
    @method_decorator(sensitive_post_parameters('private_key_passphrase'))
    def import_certificate_with_key(self, request):

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            original="Import Certificate With Key (.p12/.pfx)",
            opts=self.opts,
            change=True,
            is_popup=False,
            save_as=False,
            has_view_permission=True,
            has_delete_permission=False,
            has_add_permission=False,
            has_change_permission=False
        )

        if request.method == 'POST':

            form = self.import_form(request.POST, request.FILES)
            if form.is_valid():

                obj = form.save(commit=False)
                obj.save()

                # ToDo(frennkie) could also add link to change site of new object
                self.message_user(request, "Successfully imported: %s" % form.instance)

                certs_to_add = []
                for ca_cert in form.cleaned_data['ca_certs']:
                    new_obj = obj.ca_certs.model.load_certificate(certificate=ca_cert)

                    try:
                        old_obj = obj.ca_certs.model.objects.get(certificate_txt=new_obj.certificate_txt)
                        certs_to_add.append(old_obj)
                        log.debug("ca_cert exists already: {}".format(old_obj))
                        self.message_user(request, "CA is already known - skipping: %s" % new_obj,
                                          level=messages.WARNING)

                    except obj.ca_certs.model.DoesNotExist:
                        new_obj.save()
                        certs_to_add.append(new_obj)
                        log.debug("ca_cert was newly created: {}".format(new_obj))
                        self.message_user(request, "Successfully imported CA: %s" % new_obj)

                form.cleaned_data['ca_certs'] = certs_to_add
                form.save_m2m()

        else:
            form = self.import_form()
            log.info("showing form.")

        context.update({'form': form})

        template = 'admin/{}/{}/{}'.format(self.opts.app_label,
                                           self.opts.model_name,
                                           'import_certificate_with_key.html')
        return TemplateResponse(request, template, context)

    def is_private_key_encrypted(self, obj):
        return obj.is_private_key_encrypted

    is_private_key_encrypted.boolean = True

    def is_secret_key_unchanged(self, obj):
        return obj.is_secret_key_unchanged

    is_secret_key_unchanged.boolean = True

    def is_self_signed(self, obj):
        return obj.is_self_signed

    is_self_signed.boolean = True


admin.site.register(CaCertificate, CaCertificateAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(CertificateWithKey, CertificateWithKeyAdmin)
