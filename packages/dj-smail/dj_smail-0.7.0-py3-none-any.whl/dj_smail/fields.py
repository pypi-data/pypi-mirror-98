import hashlib
import os

from django.conf import settings
from django.core.exceptions import FieldError, ImproperlyConfigured
from django.db import models
from django.utils.encoding import force_bytes, force_str
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from dj_smail.crypto import derive_key, encrypt, decrypt

__all__ = [
    'EncryptedField',
    'EncryptedTextField',
    'EncryptedCharField'
]


class EncryptedField(models.Field):
    """A field that encrypts values using AES GCM 256-bit symmetric encryption."""

    SECRET_KEY_CHANGED = _("<SECRET KEY changed>")

    _internal_type = 'BinaryField'

    def __init__(self, *args, **kwargs):
        if kwargs.get('primary_key'):
            raise ImproperlyConfigured(
                "%s does not support primary_key=True."
                % self.__class__.__name__
            )
        if kwargs.get('unique'):
            raise ImproperlyConfigured(
                "%s does not support unique=True."
                % self.__class__.__name__
            )
        if kwargs.get('db_index'):
            raise ImproperlyConfigured(
                "%s does not support db_index=True."
                % self.__class__.__name__
            )
        super(EncryptedField, self).__init__(*args, **kwargs)

    @cached_property
    def symmetric_key_from_secret_key(self):
        if len(settings.SECRET_KEY) < 10:
            raise ImproperlyConfigured("SECRET_KEY MUST be at least 10 characters long.")
        return derive_key(settings.SECRET_KEY.encode())

    @cached_property
    def secret_key_hash(self):
        return hashlib.sha256(settings.SECRET_KEY.encode()).digest()

    def get_internal_type(self):
        return self._internal_type

    def get_db_prep_save(self, value, connection):
        value = super(EncryptedField, self).get_db_prep_save(value, connection)
        if value is not None:
            nonce = os.urandom(16)
            # TODO(frennkie) adding a (single-round) sha256 hash of secret key might not be a good idea
            encrypted_value = encrypt(force_bytes(value), self.symmetric_key_from_secret_key, nonce)

            ret_val = self.secret_key_hash + nonce + encrypted_value

            return connection.Database.Binary(ret_val)

    def from_db_value(self, value, expression, connection, *args):
        if value is not None:
            # check whether hash of secret key in db matches current application secret key hash
            secret_key_hash_from_db = value[:len(self.secret_key_hash)]
            if not secret_key_hash_from_db == self.secret_key_hash:
                return self.SECRET_KEY_CHANGED

            nonce = value[len(self.secret_key_hash):len(self.secret_key_hash) + 16]
            value = value[len(self.secret_key_hash) + 16:]

            value = bytes(value)
            decrypted_value = decrypt(force_bytes(value), self.symmetric_key_from_secret_key, nonce)
            return self.to_python(force_str(decrypted_value))

    @cached_property
    def validators(self):
        # Temporarily pretend to be whatever type of field we're masquerading
        # as, for purposes of constructing validators (needed for
        # IntegerField and subclasses).
        self.__dict__['_internal_type'] = super(
            EncryptedField, self
        ).get_internal_type()
        try:
            return super(EncryptedField, self).validators
        finally:
            del self.__dict__['_internal_type']


def get_prep_lookup(self):
    """Raise errors for unsupported lookups"""
    raise FieldError("{} '{}' does not support lookups".format(
        self.lhs.field.__class__.__name__, self.lookup_name))


# Register all field lookups (except 'isnull') to our handler
for name, lookup in models.Field.get_lookups().items():
    # Dynamically create classes that inherit from the right lookups
    if name != 'isnull':
        lookup_class = type('EncryptedField' + name, (lookup,), {
            'get_prep_lookup': get_prep_lookup
        })
        EncryptedField.register_lookup(lookup_class)


class EncryptedTextField(EncryptedField, models.TextField):
    pass


class EncryptedCharField(EncryptedField, models.CharField):
    pass
