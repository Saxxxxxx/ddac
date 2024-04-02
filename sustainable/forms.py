from django import forms
from .models import SustainableMarketplaceListing

class SustainableMarketplaceListingForm(forms.ModelForm):
    class Meta:
        model = SustainableMarketplaceListing
        fields = ['title', 'description', 'price', 'images', 'price', 'state_id', 'country_id', 'category_id']