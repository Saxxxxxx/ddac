from django.db import models
from account.models import User

import uuid

class AuditInfoDeleted(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="%(class)s_created_by_user")
    date_created = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="%(class)s_changed_by_user")
    date_changed = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True, default=False)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="%(class)s_retired_by_user")
    date_deleted = models.DateTimeField(blank=True, null=True)
    delete_reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

class Utilities():
    def generate_uuid():
        return str(uuid.uuid4())