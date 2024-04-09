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

class CustomLoginForm(forms.Form):
    email = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
    )
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','phone_number','password1','password2','avatar')

class ModifyUserForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'id': 'modify_email', 'name': 'modify_email'})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'id': 'modify_username', 'name': 'modify_username'})
    )
    first_name = forms.CharField(
        required=False,  # Setting the field as not required
        max_length=150,
        widget=forms.TextInput(attrs={'id': 'modify_first_name', 'name': 'modify_first_name'})
    )
    last_name = forms.CharField(
        required=False,  # Setting the field as not required
        max_length=150,
        widget=forms.TextInput(attrs={'id': 'modify_last_name', 'name': 'modify_last_name'})
    )
    avatar = forms.ImageField(
        required=False,  # Setting the field as not required
        widget=forms.ClearableFileInput(attrs={'id': 'modify_avatar'})  # Use ClearableFileInput
    )

    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name', 'avatar')
# class SignupForm(forms.ModelForm):
#     email = forms.EmailField(
#         required=True,
#     )
#     class Meta:
#         model = CustomNonApprovedUser
#         fields = ('username','email','first_name','last_name','password1','password2','phone_number')