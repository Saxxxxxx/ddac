from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,get_object_or_404,redirect
from sustainable.models import SustainableMarketplaceListing
from account.models import User
from food.models import FoodSharingListing
from general.models import Country,ScheduleMaintenance
from django.http import JsonResponse
from .forms import ScheduleMaintenanceForm,UpdateScheduleMaintenanceForm
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from ddac_application.settings import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_SESSION_TOKEN,ARN_USER
from ddac_application.aws import SNSUtilities



# Create your views here.
def home(request):
    return render(request,'home.html')

def about_us(request):
    return render(request,'about.html')

def profile(request):
    return render(request,'profile.html')

@staff_member_required
def admin_home(request):
    sustainable_chart_data = get_sustainable_chart_data()
    user_chart_data = get_user_chart_data()
    food_chart_data = get_food_chart_data()
    
    return render(request,'admin_home.html',context={'sustainable_chart_data':sustainable_chart_data,'user_chart_data':user_chart_data,'food_chart_data':food_chart_data})

@staff_member_required
def admin_maintenance(request):
    maintenance =ScheduleMaintenance.objects.exclude(status='Done').order_by('time')
    sns_utils = SNSUtilities
    if request.method == 'POST':
        print(request.POST)
        if 'create_schedule' in request.POST:
            print("Hi")
            form = ScheduleMaintenanceForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        form.save()
                        # Retrieve the saved data from the form
                        time = form.cleaned_data['time']
                        description = form.cleaned_data['content']
                        print(time)

                        # Trigger SNS notification
                        message = (
                            f"Scheduled Maintenance:\n"
                            f"Date: {time.strftime('%Y-%m-%d')}\n"  # Format the date as 'YYYY-MM-DD'
                            f"Time: {time.strftime('%H:%M:%S')} (UTC+8)\n"  # Format the time in Singapore timezone
                            f"Description: {description}"
                        )
                        subject = "Maintenance Scheduled"
                        SNSUtilities.send_notification(message, subject, ARN_USER)
                        messages.success(request, 'Successfully Scheduled for maintenance')

                        return redirect('admin_maintenance')  # Redirect to a success page after form submission
                except Exception as e:
                    print(e)
                    messages.warning(request, f'An error occurred: {str(e)}')
                    return redirect('admin_maintenance')
        elif 'in_progress_schedule'in request.POST:
            schedule_maintenance = ScheduleMaintenance.objects.get(id=request.POST.get('in_progress_schedule_id'))
            schedule_maintenance.status = "In Progress"
            time = schedule_maintenance.time
            description = schedule_maintenance.content
             # Trigger SNS notification
            message = (
                f"Scheduled Maintenance is in progress:\n"
                f"Date: {time.strftime('%Y-%m-%d')}\n"  # Format the date as 'YYYY-MM-DD'
                f"Time: {time.strftime('%H:%M:%S')} (UTC+8)\n"  # Format the time in Singapore timezone
                f"Description: {description}"
            )
            subject = "Maintenance In Progress"
            SNSUtilities.send_notification(message, subject, ARN_USER)
            schedule_maintenance.save()
            messages.success(request, 'Updated status')

            return redirect('admin_maintenance')  # Redirect to a success page after form submission
        elif 'complete_schedule'in request.POST:
            schedule_maintenance = ScheduleMaintenance.objects.get(id=request.POST.get('complete_schedule_id'))
            schedule_maintenance.status = "Done"
            time = schedule_maintenance.time
            description = schedule_maintenance.content
             # Trigger SNS notification
            message = (
                f"Scheduled Maintenance has been completed:\n"
                f"Date: {time.strftime('%Y-%m-%d')}\n"  # Format the date as 'YYYY-MM-DD'
                f"Time: {time.strftime('%H:%M:%S')} (UTC+8)\n"  # Format the time in Singapore timezone
                f"Description: {description}"
            )
            subject = "Maintenance Completed"
            SNSUtilities.send_notification(message, subject, ARN_USER)
            schedule_maintenance.save()
            messages.success(request, 'Updated status')

            return redirect('admin_maintenance')  # Redirect to a success page after form submission

        elif 'delete_schedule' in request.POST:
            schedule_maintenance = ScheduleMaintenance.objects.get(id=request.POST.get('delete_schedule_id'))
             # Trigger SNS notification
            message = (
                f"Scheduled Maintenance has been aborted:\n"
                f"Date Time: {schedule_maintenance.time} (UTC+8)\n"
                f"Description: {schedule_maintenance.content}"
            )
            subject="Scheduled Maintenace Aborted"
            SNSUtilities.send_notification(message, subject, ARN_USER)
            schedule_maintenance.delete()
            messages.success(request, 'Schedule Deleted')
            return redirect('admin_maintenance')
    
    form = ScheduleMaintenanceForm()
    return render(request, 'admin_maintenance.html', {'form': form,'maintenances':maintenance})

def get_sustainable_chart_data():
 # Calculate listing counts by category
    category_counts = {}
    listings = SustainableMarketplaceListing.objects.all()
    for listing in listings:
        category_id = listing.category_id.category_id
        if category_id in category_counts:
            category_counts[category_id] += 1
        else:
            category_counts[category_id] = 1
    # Prepare response data
    category_data = []
    for category_id, count in category_counts.items():
        category_data.append({
            'category_id': category_id,
            'category_name': SustainableMarketplaceListing.objects.filter(category_id=category_id).first().category_id.category_name,
            'listing_count': count
        })

    # Calculate listing counts by status
    status_counts = {}
    for status_display, _ in SustainableMarketplaceListing.STATUS_CHOICES:
        status_counts[status_display] = listings.filter(status=status_display).count()

    # Prepare response data
    status_data = []
    for status_display, count in status_counts.items():
        status_data.append({
            'status': status_display,
            'listing_count': count
        })

    return ({'listings_by_category': category_data,'listings_by_status': status_data})

def get_user_chart_data():
    # Count number of active users
    active_users_count = User.objects.filter(is_active=True).count()

    # Count number of banned users
    banned_users_count = User.objects.filter(is_banned=True).count()

    # Count number of non-approved users
    non_approved_users_count = User.objects.filter(is_active=False).count()

    return({'number_of_active_user': active_users_count,'number_of_banned_user': banned_users_count,'number_of_non_approved_user': non_approved_users_count})

def get_food_chart_data():
    # Calculate listing counts by category
    category_counts = {}
    listings = FoodSharingListing.objects.all()
    for listing in listings:
        category_id = listing.category_id.category_id
        if category_id in category_counts:
            category_counts[category_id] += 1
        else:
            category_counts[category_id] = 1
     # Prepare response data
    category_data = []
    for category_id, count in category_counts.items():
        category_data.append({
            'category_id': category_id,
            'category_name': FoodSharingListing.objects.filter(category_id=category_id).first().category_id.category_name,
            'listing_count': count
        })

    # Calculate listing counts by status
    status_counts = {}
    for status_display, _ in FoodSharingListing.STATUS_CHOICES:
        status_counts[status_display] = listings.filter(status=status_display).count()

    # Prepare response data
    status_data = []
    for status_display, count in status_counts.items():
        status_data.append({
            'status': status_display,
            'listing_count': count
        })

    return ({'listings_by_category': category_data,'listings_by_status': status_data})

def get_country(request):
    countries = Country.objects.all()
    country_list = []
    for country in countries:
        country_data = {
            'country_id': country.country_id,
            'country_name': country.country_name,
            'uuid': str(country.uuid),
            'states': []
        }
        # Fetch states for the current country
        states = country.states.all()
        for state in states:
            state_data = {
                'state_id': state.state_id,
                'state_name': state.state_name,
                'uuid': str(state.uuid),
            }
            country_data['states'].append(state_data)
        country_list.append(country_data)
    return JsonResponse(country_list, safe=False)

