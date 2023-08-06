from copy import deepcopy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives, SafeMIMEMultipart, DNS_NAME
from smail import sign_message


class SMailMessage(EmailMessage):
    sign = False
    signer_crt = None
    signer_key = None

    encrypt = False
    encrypt_to_crts = list()

    @classmethod
    def from_email_message(cls, msg: EmailMessage):
        # ToDo(frennkie) is there a solid and smarter way to do this?
        return cls(
            subject=msg.subject,
            body=msg.body,
            from_email=msg.from_email,
            to=deepcopy(msg.to),
            bcc=deepcopy(msg.bcc),
            connection=msg.connection,
            attachments=deepcopy(msg.attachments),
            headers=deepcopy(msg.extra_headers),
            cc=deepcopy(msg.cc),
            reply_to=deepcopy(msg.reply_to)
        )

    def message(self):
        msg = super().message()
        if self.sign and self.signer_crt and self.signer_key:
            signed_msg = sign_message(msg, self.signer_key, self.signer_crt,
                                      multipart_class=SafeMIMEMultipart)

            return signed_msg

        else:
            return msg


class SMailMultiAlternatives(EmailMultiAlternatives):
    sign = False
    signer_crt = None
    signer_key = None

    encrypt = False
    encrypt_to_crts = list()

    @classmethod
    def from_email_message(cls, msg: EmailMultiAlternatives):
        # ToDo(frennkie) is there a solid and smarter way to do this?
        return cls(
            subject=msg.subject,
            body=msg.body,
            from_email=msg.from_email,
            to=deepcopy(msg.to),
            bcc=deepcopy(msg.bcc),
            connection=msg.connection,
            attachments=deepcopy(msg.attachments),
            headers=deepcopy(msg.extra_headers),
            alternatives=deepcopy(msg.alternatives),
            cc=deepcopy(msg.cc),
            reply_to=deepcopy(msg.reply_to)
        )

    def message(self):
        msg = super().message()
        if self.sign and self.signer_crt and self.signer_key:

            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.subject
            msg['From'] = self.extra_headers.get('From', self.from_email)
            self._set_list_header_if_not_empty(msg, 'To', self.to)
            self._set_list_header_if_not_empty(msg, 'Cc', self.cc)
            self._set_list_header_if_not_empty(msg, 'Reply-To', self.reply_to)

            # Email header names are case-insensitive (RFC 2045), so we have to
            # accommodate that when doing comparisons.
            header_names = [key.lower() for key in self.extra_headers]
            if 'date' not in header_names:
                # formatdate() uses stdlib methods to format the date, which use
                # the stdlib/OS concept of a timezone, however, Django sets the
                # TZ environment variable based on the TIME_ZONE setting which
                # will get picked up by formatdate().
                msg['Date'] = formatdate(localtime=settings.EMAIL_USE_LOCALTIME)
            if 'message-id' not in header_names:
                # Use cached DNS_NAME for performance
                msg['Message-ID'] = make_msgid(domain=DNS_NAME)
            for name, value in self.extra_headers.items():
                if name.lower() != 'from':  # From is already handled
                    msg[name] = value

            msg.preamble = 'This is a multi-part message in MIME format.'

            # Encapsulate the plain and HTML versions of the message body in an
            # 'alternative' part, so message agents can decide which they want to display.
            msg_alternative = MIMEMultipart('alternative')
            msg.attach(msg_alternative)

            msg_text = MIMEText(self.body)
            msg_alternative.attach(msg_text)

            if self.alternatives:
                try:
                    # ToDo(frennkie) can there be multiple alternatives?!
                    msg_html = MIMEText(self.alternatives[0][0], 'html')
                    msg_alternative.attach(msg_html)
                except IndexError:
                    pass

            signed_msg = sign_message(msg, self.signer_key, self.signer_crt,
                                      multipart_class=SafeMIMEMultipart)

            return signed_msg

        else:
            return msg
