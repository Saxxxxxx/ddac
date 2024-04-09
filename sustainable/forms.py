from django import forms
from .models import SustainableMarketplaceListing
from general.models import State

class SustainableMarketplaceListingForm(forms.ModelForm):
    class Meta:
        model = SustainableMarketplaceListing
        fields = ['title', 'description', 'price', 'images', 'price', 'state_id', 'country_id', 'category_id']

# class SustainableListingForm(forms.ModelForm):
#     class Meta:
#         model = SustainableMarketplaceListing
#         fields = ['title', 'description', 'price', 'category_id', 'state_id', 'country_id', 'images']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
#             'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
#             'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a category'}),
#             'state': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a state'}),
#             'country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a country'}),
#             'images': forms.FileField(widget = forms.TextInput(attrs={
#             "name": "images",
#             "type": "File",
#             "class": "form-control",
#             "multiple": "True",
#         }), label = "")
#         }
    # class Meta:
    #     model = SustainableMarketplaceListing
    #     fields = ['title', 'description', 'price', 'images', 'price', 'state_id', 'country_id', 'category_id','user']
    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields['state_id'].queryset = State.objects.none()

# class ModifySustainableListingForm(forms.ModelForm):
#     class Meta:
#         model = SustainableMarketplaceListing
#         fields = ['title', 'description', 'price', 'category', 'state', 'country', 'images']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
#             'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
#             'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a category'}),
#             'state': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a state'}),
#             'country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select a country'}),
#             'images': forms.FileField(widget = forms.TextInput(attrs={
#             "name": "images",
#             "type": "File",
#             "class": "form-control",
#             "multiple": "True",
#         }), label = "")
#         }