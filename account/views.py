import json
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set is_active to False initially
            user.save()
            # Create a new permission group
            group, created = Group.objects.get_or_create(name='User')  # Replace 'YourGroup' with the name of your group
            # login(request,new_user)
            # Add the user to the group
            user.groups.add(group)
            messages.success(request, 'Successful Registered. Wait For Approval From Admin')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request,'registration/signup.html',{'form':form})

def view_profile(request):
    #LOAD PROFILE FROM REQUEST USER
    #ONCE LOAD DO MULTIPLE POST ON MODIFY PROFILE, MODIFY SUSTAINABLE LISTING, AND MODIFY FOOD LIST
    if request.method == 'POST':
        return redirect('login')
    else:
        edit_profile_form = EditProfileForm()
    return render(request,'profile.html',{'edit_profile_form':edit_profile_form})