from django import forms
from .models import FoodSharingListing

class FoodSharingListingForm(forms.ModelForm):
    class Meta:
        model = FoodSharingListing
        fields = ['title', 'description', 'price', 'street_address', 'postal_code', 'state_id', 'country_id', 'held_date', 'expiration_date', 'category_id', 'status']

    # def __init__(self, *args, **kwargs):
    #     super(FoodSharingListingForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Submit'))