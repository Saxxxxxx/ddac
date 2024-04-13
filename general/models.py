from django.db import models

# from account.models import User

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
    
class ScheduleMaintenance(models.Model):
    class Meta:
        db_table="schedule_maintenance"
    # Define choices for the status field
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ]
    id = models.AutoField(primary_key=True)
    content = models.CharField()
    time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
