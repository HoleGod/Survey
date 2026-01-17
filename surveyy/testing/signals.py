from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Test, UserTest
from .services.exel_export import create_exel

@receiver(post_save, sender=Test)
def save_xlsx(sender, instance, created, **kwargs):
    create_exel(instance)