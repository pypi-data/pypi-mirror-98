from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand


def encrypt(cleartext, key, nonce):
    """Encrypts cleartext (bytes) using key and nonce"""
    aesgcm = AESGCM(key)
    return aesgcm.encrypt(nonce, cleartext, None)


def decrypt(ciphertext, key, nonce):
    """Decrypts ciphertext (bytes) using key and nonce"""
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)


def derive_key(strong_passphrase):
    """Derives a 256 bit key from a strong byte string"""
    hkdf = HKDFExpand(
        algorithm=hashes.SHA256(),
        length=32,
        info=None,
        backend=default_backend()
    )
    return hkdf.derive(strong_passphrase)
