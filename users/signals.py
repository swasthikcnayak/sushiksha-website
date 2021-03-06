from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.tasks import send_email
from .models import Profile, Pomodoro, Reward


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Pomodoro.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Reward)
def send_mail(sender, instance, created, **kwargs):
    if created:
        email = instance.user.email
        name = instance.user.profile.name
        badge = instance.badges.title
        description = instance.description
        awarded_by = instance.awarded_by
        timestamp = instance.timestamp
        image = 'https://sushiksha.konkanischolarship.com' + str(instance.badges.logo.url)
        array = [email, timestamp, awarded_by, description, badge, name, image]
        send_email.delay(array)
        # do not uncomment
        # uncomment above line only if you have celery, rabbitmq setup and know the implementation
        return True
