import email
from copy import deepcopy

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import pkcs7


def sign_message(message, key_signer, cert_signer):
    """Takes a message, signs it and returns a new signed message object.

    Args:
        message (:obj:`email.message.Message`): The message object to sign.
        key_signer (:obj:`cryptography.hazmat.primitives.asymmetric.ec.RSAPrivateKey` or
            :obj:`cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePrivateKey`): Private
            key used to sign the message.
        cert_signer (:obj:`cryptography.x509.Certificate`): Certificate/Public Key (belonging to
            Private Key) that will be included in the signed message.

    Returns:
         :obj:`email.message.Message`: signed message

    """

    assert isinstance(key_signer, (RSAPrivateKey, EllipticCurvePrivateKey))
    assert isinstance(cert_signer, x509.Certificate)

    # make a deep copy of original message to avoid any side effects (original will not be touched)
    copied_msg = deepcopy(message)

    headers = {}
    # besides some special ones (e.g. Content-Type) remove all headers before signing the body content
    for hdr_name in copied_msg.keys():
        if hdr_name in ["Content-Type", "Content-Transfer-Encoding"]:
            continue

        values = copied_msg.get_all(hdr_name)
        if values:
            del copied_msg[hdr_name]
            headers[hdr_name] = values

    data_unsigned = copied_msg.as_string().encode()
    data_unsigned = data_unsigned.replace(b'\n', b'\r\n')

    options = [pkcs7.PKCS7Options.DetachedSignature]
    data_signed = pkcs7.PKCS7SignatureBuilder().set_data(
        data_unsigned
    ).add_signer(
        cert_signer, key_signer, hashes.SHA256()
    ).sign(
        serialization.Encoding.PEM, options
    )

    # parse into Message object
    new_msg = email.message_from_bytes(data_signed)

    # (re-)add original headers
    for hdr, values in headers.items():
        for val in values:
            new_msg.add_header(hdr, str(val))

    return new_msg
