from django.db import models

from general.utils import *

# Create your models here.
class Country(AuditInfoDeleted):
    class Meta:
        db_table="country"
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100)
    uuid = models.UUIDField(max_length=38, blank=False, null=False, unique=True,default=uuid.uuid4, editable=False)
    def __str__(self):
        return self.country_name


class State(AuditInfoDeleted):
    class Meta:
        db_table="state"
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=100)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    uuid = models.UUIDField(max_length=38, blank=False, null=False, unique=True,default=uuid.uuid4, editable=False)
    def __str__(self):
        return self.state_name
