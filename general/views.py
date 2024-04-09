from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from sustainable.models import SustainableMarketplaceListing
from account.models import User
from food.models import FoodSharingListing
from general.models import Country
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request,'home.html')

def about_us(request):
    return render(request,'about.html')

@staff_member_required
def admin_home(request):
    sustainable_chart_data = get_sustainable_chart_data()
    user_chart_data = get_user_chart_data()
    food_chart_data = get_food_chart_data()
    
    return render(request,'admin_home.html',context={'sustainable_chart_data':sustainable_chart_data,'user_chart_data':user_chart_data,'food_chart_data':food_chart_data})


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
