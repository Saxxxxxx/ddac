from django.db import models
from account.models import User
from general.models import Country,State
from general.utils import *


class SustainableMarketplaceListingImage(models.Model):
    class Meta:
        db_table = 'sustainable_sustainablemarketplace_image'
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='sustainable_images')
    uuid = models.UUIDField(max_length=38, blank=False, null=False, unique=True,default=uuid.uuid4, editable=False)


class SustainableMarketplaceCategory(AuditInfoDeleted):
    class Meta:
        db_table = 'sustainable_sustainablemarketplace_category'
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    uuid = models.UUIDField(max_length=38, blank=False, null=False, unique=True,default=uuid.uuid4, editable=False)
    def __str__(self):
        return self.category_name
    
class SustainableMarketplaceListing(AuditInfoDeleted):
    class Meta:
        db_table="sustainable_marketplace_listing"
        
    listing_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ManyToManyField(SustainableMarketplaceListingImage)  # Many-to-many relationship with Image model
    price = models.DecimalField(max_digits=10, decimal_places=2)
    state_id = models.ForeignKey(State,on_delete=models.CASCADE, related_name='sustainable_marketplace_state_id')
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='sustainable_marketplace_country_id')
    uuid = models.UUIDField(max_length=38, blank=False, null=False, unique=True,default=uuid.uuid4, editable=False)
    category_id = models.ForeignKey(SustainableMarketplaceCategory, on_delete=models.CASCADE, related_name='sustainable_marketplace_category_id')
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Claimed', 'Claimed'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

