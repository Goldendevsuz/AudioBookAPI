from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.user.utils import generate_code

User = get_user_model()


@receiver(post_save, sender=User)
def send_email(sender, instance, created, **kwargs):
    code = generate_code()
    cache.set(f"{instance.pk}", code, timeout=300)
    redirect_url = f"{settings.BASE_URL}/api/user/verify-code?code={code}&user_id={instance.pk}"
    subject = 'Welcome to Our Site!'
    message = f'verify code: {code} url: {redirect_url}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [instance.email]

    send_mail(subject, message, from_email, recipient_list)
