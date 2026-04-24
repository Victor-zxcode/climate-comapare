"""Custom model mixins"""
from django.db import models
from django.utils import timezone


class TimestampedMixin(models.Model):
    """Mixin that adds created_at and updated_at fields"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """Mixin that adds soft delete functionality"""

    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete by setting deleted_at"""
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore soft-deleted object"""
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        """Check if object is soft-deleted"""
        return self.deleted_at is not None
