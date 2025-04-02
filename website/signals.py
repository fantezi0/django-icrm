from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Item
from .hashmap import HashMapManager

# Create a HashMapManager instance

# Register an item in the HashMapManager on item creation
@receiver(post_save, sender=Item)
def update_hash_map(sender, instance, created, **kwargs):
    print(f"signal triggered for {instance}")
    if created:
        HashMapManager.add_to_map(instance)
