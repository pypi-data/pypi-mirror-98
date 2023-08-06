import webbrowser
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.console import EmailBackend as ConsoleBackend
from django.core.mail.backends.filebased import EmailBackend as FileBackend
from django.core.mail.backends.locmem import EmailBackend as LocmemBackend
from django.core.mail.backends.smtp import EmailBackend as SmtpBackend


class BrowsableEmailBackend(BaseEmailBackend):
    """
    An email backend that opens HTML parts of emails sent
    in a local web browser, for testing during development.
    """

    def send_messages(self, email_messages):
        if not settings.DEBUG:
            # Should never be used in production.
            return
        for message in email_messages:
            for body, content_type in getattr(message, "alternatives", []):
                if content_type == "text/html":
                    self.open(body)

    def open(self, body=None):
        if body:
            with NamedTemporaryFile(delete=False) as temp:
                temp.write(body.encode('utf-8'))

            webbrowser.open("file://" + temp.name)


class EncryptingEmailBackendMixin(object):
    def send_messages(self, email_messages):
        print(f"Sending from: {self.__class__.__name__} ...")
        # noinspection PyUnresolvedReferences
        super(EncryptingEmailBackendMixin, self).send_messages(email_messages)


class EncryptingConsoleEmailBackend(EncryptingEmailBackendMixin, ConsoleBackend):
    pass


class EncryptingLocmemEmailBackend(EncryptingEmailBackendMixin, LocmemBackend):
    pass


class EncryptingFilebasedEmailBackend(EncryptingEmailBackendMixin, FileBackend):
    pass


class EncryptingSmtpEmailBackend(EncryptingEmailBackendMixin, SmtpBackend):
    pass
