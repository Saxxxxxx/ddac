from django import forms

from .models import User

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django import forms

# from django import forms

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','phone_number','password1','password2')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','avatar')

# class SignupForm(forms.ModelForm):
#     email = forms.EmailField(
#         required=True,
#     )
#     class Meta:
#         model = CustomNonApprovedUser
#         fields = ('username','email','first_name','last_name','password1','password2','phone_number')