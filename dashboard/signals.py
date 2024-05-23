from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Subprofile

@receiver(post_save, sender=Profile)
def create_subprofile(sender, instance, created, **kwargs):
    if created:
        Subprofile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def save_subprofile(sender, instance, **kwargs):
    instance.subprofile.save()
