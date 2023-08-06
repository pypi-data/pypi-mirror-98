from os.path import splitext

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12
from django import forms
from django.utils.translation import gettext_lazy as _

from dj_smail.models import CaCertificate, Certificate, CertificateWithKey


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ('certificate_txt',)

        # help_texts for properties
        help_texts = {
            'cn': 'x.509 Subject: Common Name',
            'san_email': 'x.509 Subject Alternative Name: e-emailAddress',
        }

        # labels for properties
        labels = {
            'cn': 'Common Name',
            'is_root_ca': _('Is Root CA?'),
            'is_intermediate_ca': _('Is Intermediate CA?'),
            'is_end_entity': _('Is End Entity?'),
            'san_email': _('SAN eMail'),
            'fingerprint_sha256': _('Fingerprint (SHA256)')
        }

        widgets = {
            'certificate_txt': forms.Textarea(attrs={'class': 'pem-textfield',
                                                     'cols': '68', 'rows': '6'}),
        }


class CaCertificateForm(CertificateForm):
    class Meta(CertificateForm.Meta):
        model = CaCertificate


class CertificateWithKeyForm(CertificateForm):
    class Meta(CertificateForm.Meta):
        model = CertificateWithKey

        fields = CertificateForm.Meta.fields + ('private_key_txt',
                                                'private_key_passphrase',
                                                'ca_certs')

        # labels for properties
        labels = CertificateForm.Meta.labels

        labels.update({
            'is_private_key_encrypted': _('Is Private Key encrypted?'),
        })

        CertificateForm.Meta.widgets.update({
            'private_key_txt': forms.Textarea(attrs={'class': 'pem-textfield',
                                                     'cols': '68', 'rows': '6'}),
            'private_key_passphrase': forms.PasswordInput(),
        })


class CertificateImportForm(forms.ModelForm):
    SUPPORTED_EXT = ['.cer', '.crt', '.der', '.pem', '.txt']

    file = forms.FileField(
        label='File',
        label_suffix=':',
        help_text=_('Certificate File (.cer, .crt, .der, .pem, .txt)'),
        required=True,
    )

    class Meta(CertificateForm.Meta):
        model = Certificate
        fields = ('file',
                  'certificate_txt')

        widgets = {
            'certificate_txt': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CertificateImportForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['certificate_txt'].required = False

    def clean(self):
        super(CertificateImportForm, self).clean()
        file = self.cleaned_data.get('file')

        try:
            file_name = splitext(file.name)
            if file_name[-1] not in self.SUPPORTED_EXT:
                raise forms.ValidationError('Supported extensions: {}.'.format(", ".join(self.SUPPORTED_EXT)))
        except (AttributeError, IndexError):
            pass

        certificate = x509.load_pem_x509_certificate(file.read(), backend=default_backend())
        obj = self.instance.load_certificate(certificate)

        self.cleaned_data['certificate_txt'] = obj.certificate_txt
        self.cleaned_data['obj'] = obj

        return self.cleaned_data


class CaCertificateImportForm(CertificateImportForm):
    class Meta(CertificateImportForm.Meta):
        model = CaCertificate

    def clean(self):
        super(CaCertificateImportForm, self).clean()
        obj = self.cleaned_data.get('obj')

        if not obj.is_certificate_authority:
            raise forms.ValidationError('Import Certificate is not a Root or Intermediate '
                                        'Certificate Authority.')

        return self.cleaned_data


class CertificateWithKeyImportForm(forms.ModelForm):
    file = forms.FileField(
        label='File',
        label_suffix=':',
        help_text=_('Certificate with Key File (.p12 or .pfx)'),
        required=True,
    )

    private_key_passphrase = forms.CharField(
        label='Passphrase',
        label_suffix=':',
        help_text=_('The Passphrase to decrypt the private key.'),
        max_length=255,
        required=True,
        widget=forms.PasswordInput(),
    )

    class Meta(CertificateForm.Meta):
        model = CertificateWithKey
        fields = ('file',
                  'private_key_passphrase',
                  'certificate_txt', 'private_key_txt', 'ca_certs')

        widgets = {
            'certificate_txt': forms.HiddenInput(),
            'private_key_txt': forms.HiddenInput(),
            'ca_certs': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CertificateWithKeyImportForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['certificate_txt'].required = False
        self.fields['private_key_txt'].required = False
        self.fields['ca_certs'].required = False

    def clean(self):
        cleaned_data = super(CertificateWithKeyImportForm, self).clean()
        file = cleaned_data.get('file')

        try:
            file_name = splitext(file.name)
            if file_name[-1] not in ['.p12', '.pfx']:
                raise forms.ValidationError('Only .p12 and .pfx supported.')
        except (AttributeError, IndexError):
            pass

        private_key_passphrase = cleaned_data.get('private_key_passphrase')
        passphrase_bytes = private_key_passphrase.encode()

        private_key, certificate, ca_certs = pkcs12.load_key_and_certificates(
            file.read(),
            password=passphrase_bytes,
            backend=default_backend()
        )

        obj = self.instance.load_certificate_with_key(
            certificate,
            private_key,
            passphrase_bytes,
        )

        self.cleaned_data['certificate_txt'] = obj.certificate_txt
        self.cleaned_data['private_key_txt'] = obj.private_key_txt
        self.cleaned_data['ca_certs'] = ca_certs

        # return self.cleaned_data
