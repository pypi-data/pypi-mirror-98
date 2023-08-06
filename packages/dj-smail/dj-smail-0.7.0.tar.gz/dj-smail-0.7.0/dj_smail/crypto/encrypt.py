# _*_ coding: utf-8 _*_
import base64
import os
from copy import deepcopy
from email import message_from_string, message_from_bytes
from email.mime.text import MIMEText

from asn1crypto import cms
from asn1crypto.x509 import Certificate as AsnCryptoCertificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.x509 import Certificate


class UnsupportedAlgorithmError(Exception):
    """
    An exception indicating that an unsupported cipher algorithm was specified
    """

    pass


def iterate_recipient_info_for_certs(certs, session_key, key_enc_alg):
    """Yields the recipient info data needed for an encrypted message.

    Args:
        certs (:obj:`list` of :obj:`cryptography.x509.Certificate`): Certificate object
        session_key (bytes): Session key
        key_enc_alg (str): Key Encryption Algorithm

    Yields:
        :obj:`asn1crypto.cms.KeyTransRecipientInfo`

    """

    for cert in certs:
        yield get_recipient_info_for_cert(cert, session_key, key_enc_alg)


def get_recipient_info_for_cert(cert, session_key, key_enc_alg="rsaes_pkcs1v15"):
    """Returns the recipient identifier data needed for an encrypted message.

    Args:
        cert (:obj:`cryptography.x509.Certificate`): Certificate object
        session_key (bytes): Session key
        key_enc_alg (str): Key Encryption Algorithm

    Returns:
        :obj:`asn1crypto.cms.KeyTransRecipientInfo`

    """

    assert isinstance(cert, Certificate)

    # load cryptography.x509.Certificate as asn1crypto.x509.Certificate in order
    # to get issuer and serial in correct format for CMS Recipient Info object
    # noinspection PyTypeChecker
    asn1_cert = AsnCryptoCertificate.load(cert.public_bytes(Encoding.DER))

    # asymmetrically encrypt session key for recipient (identified by issuer + serial)
    encrypted_key = cert.public_key().encrypt(session_key, padding=PKCS1v15())

    return cms.KeyTransRecipientInfo({
        "version": "v0",
        "rid": cms.IssuerAndSerialNumber({
            "issuer": asn1_cert.issuer,
            "serial_number": asn1_cert.serial_number,
        }),
        "key_encryption_algorithm": {
            "algorithm": key_enc_alg,
        },
        "encrypted_key": encrypted_key,
    })


def aes256_cbc(data: bytes) -> (bytes, bytes, bytes):
    # Ensure padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encode the content
    iv = os.urandom(16)
    key = os.urandom(32)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted_content = encryptor.update(padded_data) + encryptor.finalize()

    return iv, key, encrypted_content


def encrypt_message_pyca(message, certs_recipients,
                         content_enc_alg="aes256_cbc", key_enc_alg="rsaes_pkcs1v15", prefix=""):
    """Takes a message and returns a new message with the original content as encrypted body

    Take the contents of the message parameter, formatted as in RFC 2822 (type bytes, str or
        message) and encrypts them, so that they can only be read by the intended recipient
        specified by pubkey.

    Args:
        message (bytes, str or :obj:`email.message.Message`): Message to be encrypted.
        certs_recipients (:obj:`list` of `cryptography.x509.Certificate`): A list certificates.
        key_enc_alg (str): Key Encryption Algorithm
        content_enc_alg (str): Content Encryption Algorithm
        prefix (str): Content type prefix (e.g. "x-"). Default to ""

    Returns:
        :obj:`message`: The new encrypted message (type str or message, as per input).

    """

    certificates = []
    for cert in certs_recipients:
        if isinstance(cert, Certificate):
            certificates.append(cert)
        else:
            raise NotImplementedError

    if not content_enc_alg == "aes256_cbc":
        raise UnsupportedAlgorithmError("currently only AES 256 bit implemented")

    # Get the message content. This could be a string, bytes or a message object
    passed_as_str = isinstance(message, str)

    if passed_as_str:
        message = message_from_string(message)

    passed_as_bytes = isinstance(message, bytes)
    if passed_as_bytes:
        message = message_from_bytes(message)

    # Extract the message payload without conversion, & the outermost MIME header / Content headers. This allows
    # the MIME content to be rendered for any outermost MIME type incl. multipart
    copied_msg = deepcopy(message)

    headers = {}
    # besides some special ones (e.g. Content-Type) remove all headers before encrypting the body content
    for hdr_name in copied_msg.keys():
        if hdr_name in ["Content-Type", "MIME-Version", "Content-Transfer-Encoding"]:
            continue

        values = copied_msg.get_all(hdr_name)
        if values:
            del copied_msg[hdr_name]
            headers[hdr_name] = values

    content = copied_msg.as_bytes()

    # create iv, key and encrypt
    iv, key, encrypted_content = aes256_cbc(content)

    recipient_infos = []
    for recipient_info in iterate_recipient_info_for_certs(certificates, key, key_enc_alg=key_enc_alg):
        if recipient_info is None:
            raise ValueError("unable to create RecipientInfo object")
        recipient_infos.append(recipient_info)

    # Build the enveloped data and encode in base64
    ci = cms.ContentInfo(
        {
            "content_type": "enveloped_data",
            "content": {
                "version": "v0",
                "recipient_infos": recipient_infos,
                "encrypted_content_info": {
                    "content_type": "data",
                    "content_encryption_algorithm": {
                        "algorithm": content_enc_alg,
                        "parameters": iv,
                    },
                    "encrypted_content": encrypted_content,
                },
            },
        }
    )
    encoded_content = base64.encodebytes(ci.dump()).decode()

    # Create the resulting message
    result_msg = MIMEText(encoded_content)
    overrides = (
        ("MIME-Version", "1.0"),
        (
            "Content-Type",
            "application/{}pkcs7-mime; smime-type=enveloped-data; name=smime.p7m".format(prefix),
        ),
        ("Content-Transfer-Encoding", "base64"),
        ("Content-Disposition", "attachment; filename=smime.p7m"),
    )

    for name, value in list(copied_msg.items()):
        if name in [x for x, _ in overrides]:
            continue
        result_msg.add_header(name, str(value))

    for name, value in overrides:
        if name in result_msg:
            del result_msg[name]
        result_msg[name] = value

    # add original headers
    for hdr, values in headers.items():
        for val in values:
            result_msg.add_header(hdr, str(val))

    # return the same type as was passed in
    if passed_as_bytes:
        return result_msg.as_bytes()
    elif passed_as_str:
        return result_msg.as_string()
    else:
        return result_msg
