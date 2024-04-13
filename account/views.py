import json
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from ddac_application.settings import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_SESSION_TOKEN,ARN_USER
from general.utils import SNSUtilities



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
            return redirect('custom_login_page')
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


def custom_login_page(request):
    message = 'Hello'
    form = CustomLoginForm()  # Initialize the login form
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        user = User.objects.all()
        if form.is_valid():
            user_object = User.objects.get(email=form.cleaned_data['email'])
            if user_object.is_active==False:
                messages.info(request, 'Your account is not active :(')    
            else:
                user = authenticate(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                )
                if user is not None:
                    login(request, user)
                    if user.is_superuser:
                        # Redirect to custom page if user is a superuser
                        return redirect('admin_home')
                    else:
                        messages.success(request, f'Hello {user.username}! You have been logged in')    
                        return redirect('home')
            # elif user.is_superuser == False:
                else:
                    messages.warning(request, 'Incorrect Credential')
    return render(
        request, 'registration/custom-login.html', context={'form': form, 'message': message})

@staff_member_required
def admin_users(request):
    users =User.objects.filter(Q(is_active=True)&Q(is_superuser=False)).order_by('id')
    sns_utils = SNSUtilities(
        region_name='us-east-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
    if request.method == 'POST':
        if 'createUser' in request.POST:
            userForm = CreateUserForm(request.POST)
            if userForm.is_valid():
                user = userForm.save(commit=False)
                user.save()
                group, created = Group.objects.get_or_create(name='User')  # Replace 'YourGroup' with the name of your group
                user.groups.add(group)
                messages.success(request, 'Successful Registered.')
                return redirect('admin_users')
        elif 'updateUser' in request.POST:
            current_user = get_object_or_404(User,pk=request.POST.get('user_id'))
            email = current_user.email
            if request.POST.get('deleted_image'):
                # Remove the avatar from current_user
                current_user.avatar = None
                current_user.save()  # Save the changes to the user object
            mutable_post = request.POST.copy()
            mutable_post.pop('delete_image', None)  # Remove 'delete_image' from the copy
            mutable_post.pop('id', None)  # Remove 'delete_image' from the copy
            form = ModifyUserForm(mutable_post,request.FILES, instance=current_user)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        email_from_form = form.cleaned_data.get('email', None)
                        if email_from_form != email:
                            sns_utils.unsubscribe_endpoints_by_email(sns_utils.filter_subscriptions_by_email(sns_utils.get_list_of_subscriber(ARN_USER),email=email))
                            sns_utils.subscribe_user_to_sns(email_from_form, ARN_USER)
                        form.save()
                        messages.success(request, 'User has been updated.')
                except Exception as e:
                    messages.warning(request, f'An error occurred: {str(e)}')
            return redirect('admin_users')
        elif 'banUser' in request.POST:
            try:
                with transaction.atomic():
                    ban_user = User.objects.get(id=request.POST.get('user_id'))
                    ban_user.is_banned = True
                    ban_user.save()
                    sns_utils.unsubscribe_endpoints_by_email(sns_utils.filter_subscriptions_by_email(sns_utils.get_list_of_subscriber(ARN_USER),email=ban_user.email))
                messages.success(request, 'User has been banned.')
                return redirect('admin_users')
            except Exception as e:
                messages.warning(request, f'An error occurred: {str(e)}')
                return redirect('admin_users')
    userForm = CreateUserForm()
    modifyUserForm = ModifyUserForm()
    return render(request,'admin_users.html',{'users':users,'userForm':userForm,'modifyUserForm':modifyUserForm})

@staff_member_required
def admin_approve_users(request):
    users =User.objects.filter(is_active=False).order_by('id')
    # Subscribe user to SNS topic
    sns_utils = SNSUtilities(
        region_name='us-east-1',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )
    if request.method == 'POST':
        user_object = User.objects.get(pk=request.POST.get('user_id'))
        if 'approveUser' in request.POST:
            try:
                with transaction.atomic():
                    # Approve user
                    user_object.is_active = True
                    user_object.save()
                    sns_utils.subscribe_user_to_sns(user_object.email, ARN_USER)
                    # subscribe_user_to_sns(user_object)
                messages.success(request, 'User has been Approved.')
                return redirect('admin_approve_users')
            except Exception as e:
                messages.warning(request, f'An error occurred: {str(e)}')
                return redirect('admin_approve_users')
        
        elif 'rejectUser' in request.POST:
            try:
                with transaction.atomic():
                    user_object.delete()
                messages.success(request, 'User has been Rejected.')
                return redirect('admin_approve_users')
            except Exception as e:
                messages.warning(request, f'An error occurred: {str(e)}')
                return redirect('admin_approve_users')

    return render(request,'admin_approve_users.html',{'users':users})

@staff_member_required
def get_users(request):
    user_id = request.GET.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            avatar_url = user.avatar.url if user.avatar else None  # Check if user.avatar exists
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username':user.username,
                'email':user.email,
                'avatar':avatar_url
            }
            return JsonResponse({'user_data': user_data})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Listing not found'}, status=404)
    else:
        return JsonResponse({'error': 'Missing listing_id parameter'}, status=400)
    