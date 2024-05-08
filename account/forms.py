from django.db import transaction

import base64

from django import forms

from .models import User

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import AuthenticationForm, UsernameField

from django import forms

import requests

from ddac_application.aws import S3AWS



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

    def __init__(self, *args, **kwargs):
        self.delete_image = kwargs.pop('delete_image', None)  # Access the custom argument
        super(ModifyUserForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(ModifyUserForm, self).save(commit=False)
        if commit:
            user.save()
        uploaded_avatar = self.cleaned_data.get('avatar')
        deleted_avatar_data_list=[]
        if self.delete_image is not None:
            deleted_file_name = self.delete_image.name.split("/")[-1]
            deleted_file_location = User._meta.get_field('avatar').upload_to
            deleted_avatar_data = {'file_name': deleted_file_name, 'file_location': deleted_file_location}
            deleted_avatar_data_list.append(deleted_avatar_data)
        if user.avatar == self.delete_image:
            if self.delete_image is not None:
                S3AWS.delete_s3_to_api(deleted_avatar_data_list)
                user.avatar = None
                user.save()
        # Your API call to upload the avatar goes here
        elif uploaded_avatar is not None:
            avatar_data_list = []
            # Append the short UUID to the basename and rejoin with the extension
            new_file_name = user.avatar.name.split("/")[-1]
            file_location = User._meta.get_field('avatar').upload_to
            # Example API call to upload avatar
            encoded_image = base64.b64encode(uploaded_avatar.read()).decode('utf-8')
            avatar_data = {'file_name': new_file_name, 'file_location': file_location, 'image_data': encoded_image}
            avatar_data_list.append(avatar_data)
            if self.delete_image is not None:
                try:
                    S3AWS.update_s3_to_api(avatar_data_list,deleted_avatar_data_list)
                except Exception as e:
                    # Handle API call errors
                    raise Exception(f"Error uploading avatar to API: {e}")
            else:
                try:
                    S3AWS.upload_s3_to_api(avatar_data_list)
                except Exception as e:
                    # Handle API call errors
                    raise Exception(f"Error uploading avatar to API: {e}")

