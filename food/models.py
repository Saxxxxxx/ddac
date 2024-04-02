from django.db import models
from account.models import User
from general.models import Country,State
from general.utils import *

class FoodSharingListingImage(models.Model):
    class Meta:
        db_table="food_sharing_listing_image"
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='food_images')
    uuid = models.UUIDField(max_length=38, blank=False, null=False, unique=True,default=uuid.uuid4, editable=False)

class FoodSharingCategory(AuditInfoDeleted):
    class Meta:
        db_table="food_sharing_listing_category"
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    uuid = models.UUIDField(max_length=38, blank=False, null=False, unique=True,default=uuid.uuid4, editable=False)
    def __str__(self):
        return self.category_name
    
class FoodSharingListing(AuditInfoDeleted):
    class Meta:
        db_table="food_sharing_listing"
        
    listing_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ManyToManyField(FoodSharingListingImage)  # Many-to-many relationship with Image model
    price = models.DecimalField(max_digits=10, decimal_places=2)
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    state_id = models.ForeignKey(State,on_delete=models.CASCADE, related_name='food_sharing_listing_state_id')
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='food_sharing_listing_country_id')
    held_date = models.DateTimeField(blank=True,null=True)
    expiration_date = models.DateField(blank=True,null=True)
    uuid = models.UUIDField(max_length=38, blank=False, null=False, unique=True,default=uuid.uuid4, editable=False)
    category_id = models.ForeignKey(FoodSharingCategory, on_delete=models.CASCADE, related_name='food_sharing_category_id')
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Claimed', 'Claimed'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)