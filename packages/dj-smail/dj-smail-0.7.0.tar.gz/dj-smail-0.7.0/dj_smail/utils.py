from django.core.mail import EmailMultiAlternatives, EmailMessage


def get_email_message():
    return EmailMessage(
        subject='',
        body='',
        from_email=None,
        to=None,
        bcc=None,
        connection=None,
        attachments=None,
        headers=None,
        cc=None,
        reply_to=None
    )


def get_email_multi_alternatives():
    return EmailMultiAlternatives(
        subject='',
        body='',
        from_email=None,
        to=None,
        bcc=None,
        connection=None,
        attachments=None,
        headers=None,
        alternatives=None,
        cc=None,
        reply_to=None
    )
