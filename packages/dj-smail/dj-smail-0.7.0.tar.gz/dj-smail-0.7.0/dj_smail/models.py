from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.hashes import SHA256, SHA1
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, NoEncryption
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .exceptions import SecretKeyHasChangedError
from .fields import EncryptedField, EncryptedCharField


class BaseCertificate(models.Model):
    certificate_txt = models.TextField(
        verbose_name=_('Certificate'),
        help_text=_('A PEM-encoded X.509 Certificate.'),
        unique=True
    )

    serial_number = models.CharField(
        max_length=48,
        db_index=True,
        default='0',
        editable=False,
        help_text=_('The serial number of the certificate.'),
        unique=False,
        verbose_name=_('serial number'),
    )

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # store an index copy of the certificate's serial number in DB
        if self.serial_number != str(self.certificate.serial_number):
            self.serial_number = str(self.certificate.serial_number)

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return "{}".format(self.certificate.subject)

    @classmethod
    def load_certificate(cls, certificate):
        if not isinstance(certificate, x509.Certificate):
            raise ValidationError(_('Failed to load the Certificate. '
                                    'Must be of type x509.Certificate'))
        # noinspection PyTypeChecker
        cert_bytes = certificate.public_bytes(encoding=serialization.Encoding.PEM)
        cert_txt = cert_bytes.decode()
        obj = cls(certificate_txt=cert_txt)
        return obj

    def clean(self):

        try:
            if isinstance(self.certificate_txt, bytes):
                x509.load_pem_x509_certificate(self.certificate_txt, backend=default_backend())
            else:
                x509.load_pem_x509_certificate(self.certificate_txt.encode(), backend=default_backend())
        except Exception as err:
            raise ValidationError(_('Failed to load the Certificate. Error: {}'.format(err)))

    @cached_property
    def certificate(self):
        if isinstance(self.certificate_txt, bytes):
            return x509.load_pem_x509_certificate(self.certificate_txt, backend=default_backend())
        else:
            return x509.load_pem_x509_certificate(self.certificate_txt.encode(), backend=default_backend())

    @property
    def serial_hex(self):
        return hex(int(self.serial_number))[2:]

    @property
    def is_self_signed(self):
        return self.certificate.issuer == self.certificate.subject

    @property
    def is_certificate_authority(self):
        return self.certificate.extensions.get_extension_for_class(x509.BasicConstraints).value.ca  # noqa

    @property
    def is_root_ca(self):
        return self.is_self_signed and self.is_certificate_authority

    @property
    def is_intermediate_ca(self):
        return not self.is_self_signed and self.is_certificate_authority

    @property
    def is_end_entity(self):  # also known as "leaf certificate" (end of tree)
        return not self.is_certificate_authority

    @property
    def not_valid_after(self):
        return self.certificate.not_valid_after

    @property
    def not_valid_before(self):
        return self.certificate.not_valid_before

    @property
    def subject(self):
        return self.certificate.subject

    @property
    def issuer(self):
        return self.certificate.issuer

    @property
    def cn(self):
        s = self.certificate.subject.rfc4514_string().split('=')
        if s[0] == "CN":
            return s[1]
        else:
            return "N/A"

    @property
    def san(self):
        """return subject_alt_name """
        try:
            return self.certificate.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        except x509.ExtensionNotFound:
            return ""

    @property
    def _san_emails(self):
        try:
            san = self.certificate.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
            return san.get_values_for_type(x509.RFC822Name)  # noqa
        except x509.ExtensionNotFound:
            return []

    @property
    def san_email(self):
        if self._san_emails:
            return self._san_emails[0]
        else:
            return "N/A"

    @property
    def fingerprint_md5(self):
        return self.certificate.fingerprint(SHA1()).hex()

    @property
    def fingerprint_sha1(self):
        return self.certificate.fingerprint(SHA1()).hex()

    @property
    def fingerprint_sha256(self):
        return self.certificate.fingerprint(SHA256()).hex()


class BasePrivateKey(models.Model):
    private_key_txt = models.TextField(
        verbose_name=_('Private Key'),
        help_text=_('A PEM-encoded Private Key that will be stored in database in as is.'),
        unique=True
    )

    private_key_passphrase = EncryptedCharField(
        verbose_name=_('Enter Passphrase'),
        help_text=_('The Passphrase to decrypt the PEM-encoded Private Key.'),
        blank=True, null=True, max_length=255,
    )

    class Meta:
        abstract = True

    @classmethod
    def load_private_key(cls, private_key, passphrase=None):
        if not isinstance(private_key, (rsa.RSAPrivateKey, ec.EllipticCurvePrivateKey)):
            raise ValidationError(_('Failed to load the Private Key. '
                                    'Must be of type rsa.RSAPrivateKey or ec.EllipticCurvePrivateKey.'))
        if isinstance(passphrase, str):
            passphrase = passphrase.encode()

        if passphrase:
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=BestAvailableEncryption(passphrase)
            )
        else:
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=NoEncryption()
            )

        private_key_txt = private_key_bytes.decode()
        passphrase_txt = passphrase.decode()
        obj = cls(private_key_txt=private_key_txt, private_key_passphrase=passphrase_txt)
        return obj

    def clean(self):
        if self.is_private_key_encrypted and not self.private_key_passphrase:
            raise ValidationError(_('Private Key is encrypted but no passphrase is given.'))

        try:
            _p = self.private_key  # noqa
        except ValueError as err:
            raise ValidationError(_('Failed to load the Private Key. Is it valid? Error: {}'.format(err)))
        except OSError as err:
            raise ValidationError(_('Failed to load the Private Key. Possibly wrong passphrase. '
                                    'Error: {}'.format(err)))

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)

    @cached_property
    def private_key(self):
        if self.is_private_key_encrypted:
            if not self.is_secret_key_unchanged:
                raise SecretKeyHasChangedError(_(
                    "The SECRET_KEY of the application has changed. The Private Key is "
                    "no longer usable. Please re-enter the Passphrase."))

        try:
            if self.is_private_key_encrypted:
                return serialization.load_pem_private_key(self.private_key_txt.encode(),
                                                          password=self.private_key_passphrase.encode(),
                                                          backend=default_backend())
            else:
                return serialization.load_pem_private_key(self.private_key_txt.encode(),
                                                          password=None,
                                                          backend=default_backend())

        except Exception as err:
            raise ValidationError(_('Failed to load the Private Key. Possibly wrong passphrase. '
                                    'Error: {}'.format(err)))

    @property
    def is_private_key_encrypted(self):
        return "ENCRYPTED" in self.private_key_txt

    @property
    def is_secret_key_unchanged(self):
        return self.private_key_passphrase != EncryptedField.SECRET_KEY_CHANGED

    @property
    def passphrase(self):
        if self.is_private_key_encrypted:
            if self.is_secret_key_unchanged:
                return _("<REDACTED>")
            return EncryptedField.SECRET_KEY_CHANGED
        else:
            return _("No Passphrase set.")

    @property
    def algorithm(self):
        return self.private_key.algorithm

    @property
    def key_type(self):
        return type(self.private_key)


class BaseCaCertificate(BaseCertificate):
    """Represents a Certificate Authority (either Root CA or Intermediate CA)"""

    class Meta:
        abstract = True

    def clean(self):
        super().clean()

        if not self.is_certificate_authority:
            raise ValidationError(_('Certificate is not a Certificate Authority.'))


class BaseLeafCertificate(BaseCertificate):
    """Represents a (non CA) Certificate"""

    class Meta:
        abstract = True

    def clean(self):
        super().clean()

        if self.is_certificate_authority:
            raise ValidationError(_('Certificate is a Certificate Authority.'))


class BaseCertificateWithKey(BaseLeafCertificate, BasePrivateKey):
    """Represents a combination of Private Key and x.509 Certificate (=signed Public Key)

    ToDo(frennkie): check for basic constraints and extended key usages (should have non redup
        or include the signing stuff)

    """

    ca_certs = models.ManyToManyField('CaCertificate', blank=True,
                                      verbose_name=_('CA Certs'),
                                      help_text=_('List of Root or Intermediate Certificate Authorities.'))

    class Meta:
        abstract = True

    @classmethod
    def load_certificate_with_key(cls, certificate, private_key, passphrase=None, ca_certs=None):
        crt = cls.load_certificate(certificate)
        pk = cls.load_private_key(private_key, passphrase)
        obj = cls(certificate_txt=crt.certificate_txt,
                  private_key_txt=pk.private_key_txt,
                  private_key_passphrase=pk.private_key_passphrase)
        # if ca_certs:
        #     obj.ca_certs.set(ca_certs)
        return obj

    def clean(self):
        super().clean()

        if not self.cert_and_key_match:
            raise ValidationError(_('Certificate and Private Key do not belong to each other.'))

    # def __str__(self):
    #     if self.cn and self.san_email:
    #         return "CN: {} ({})".format(self.cn, self.san_email)
    #     elif self.cn:
    #         return "CN: {}".format(self.cn)
    #     elif self.san_email:
    #         return self.san_email
    #     else:
    #         return "{} object ({})".format(self.__class__.__name__, self.id)

    # cert and key check
    @property
    def cert_and_key_match(self):
        return self.certificate.public_key().public_numbers() == self.private_key.public_key().public_numbers()


class CaCertificate(BaseCertificate):
    """Represents a Certificate Authority (either Root CA or Intermediate CA)"""

    class Meta:
        verbose_name_plural = _('Root and Intermediate Certificates')


class Certificate(BaseLeafCertificate):
    """Represents a (non CA) Certificate"""

    class Meta:
        verbose_name_plural = _('Certificates')


class CertificateWithKey(BaseCertificateWithKey):
    """Represents a combination of Private Key and x.509 Certificate (=signed Public Key)

    """

    class Meta:
        verbose_name_plural = _('Certificates with Key')
