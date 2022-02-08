from django.conf import settings
from django.core.mail import EmailMessage


def send_mail(data, to):
    message = EmailMessage(
        subject='¡Recordatoria del Menu de hoy!',
        body=data,
        to=to,
        from_email=settings.EMAIL_HOST_USER,
    )
    message.content_subtype = "html"
    try:
        message.send()
    except Exception as e:
        print(str(e))
        raise Exception(str(e))