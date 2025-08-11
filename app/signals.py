from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message

@receiver(post_save, sender=Message)
def message_created(sender, instance, created, **kwargs):
    if created:
        print(f"New message in {instance.room.name} from {instance.sender.username}: {instance.content}")
