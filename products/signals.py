from django.db.models import signals
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

from .. import tasks
from .models import Ingredient


@receiver(signals.post_save, sender=Ingredient)
def update_ingredient(sender, instance, **kwargs):
    """Update ingredients index on added or chanched entries."""
    tasks.add_to_ingrs_index(instance)


@receiver(signals.post_delete, sender=Ingredient)
def delete_ingredient(sender, instance, **kwargs):
    """Update ingredients index on deleted entries."""
    tasks.delete_from_ingrs_index(instance)
