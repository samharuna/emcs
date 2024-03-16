from django.db.models.signals import post_save
from django.dispatch import receiver
from backend.models import Profile
from account.models import User
# from django.core.mail import send_mail
# from django.conf import settings


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)    

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    