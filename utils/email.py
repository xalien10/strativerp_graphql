from django.core.mail import EmailMessage


def send_email(subject, body, to, send_from='mail@strativ.se'):
    msg = EmailMessage(subject=subject, body=body, from_email=send_from, to=to)
    msg.content_subtype = "html"
    msg.send()
