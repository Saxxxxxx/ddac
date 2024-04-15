from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch, Q, F, ExpressionWrapper, DateTimeField, Count
from django.db.models.functions import TruncDate
from general.models import State,Country
from .models import FoodSharingListing,FoodSharingCategory,FoodSharingListingImage
from .forms import FoodSharingListingForm
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
import re


def filter_view(request):
    data = FoodSharingListing.objects.all()

    # Get filter parameters from the request
    category = request.GET.get('category')
    location = request.GET.get('location')
    status = request.GET.get('status')

    # Filter data based on provided parameters
    if category:
        data = data.filter(category=category)
    if location:
        data = data.filter(location=location)
    if status:
        data = data.filter(status=status)

    # Context data to pass to the template
    context = {
        'data': data,
        'selected_category': category,
        'selected_location': location,
        'selected_status': status,
    }

    return render(request, 'food_list.html', {'data': data, 'selected_category': category, 'selected_location': location, 'selected_status': status})
# Create your views here.
def food_list(request):
    images = []
    food_list = FoodSharingListing.objects.filter(Q(deleted=False) | Q(deleted__isnull=True))
    if request.GET.get('category'):
        category = request.GET.get('category')
        print(category) 
        food_list = food_list.filter(category_id__category_name=category)

    if request.GET.get('location'):
        location = request.GET.get('location')
        food_list = food_list.filter(state_id__state_name=location)
    if request.GET.get('status'):
        status = request.GET.get('status')
        food_list = food_list.filter(status=status)
    print(food_list)
    for listing in food_list:
    # Accessing all images associated with the listing
        images = listing.images.all()
    # Looping through each image
        for image in images:
        # Accessing image attributes
            image_url = image.image
            print(image_url)
        # Do whatever you need with the image_id and image_url
    create_food_form = ''
    #NEED TO CHECK IF USER IS LOGIN, IF NOT LOGIN CANT CREATE 
    if request.method == 'POST':
        if 'addListing' in request.POST:
            # create_food_form = FoodSharingListingForm(request.POST)
            # if create_food_form.is_valid():
            #     # Save the form data
            #     create_food_form.save(commit=False)
            print(request.POST)
            user = request.user  # Assuming user is authenticated
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            category_id = request.POST.get('category')
            state_id = request.POST.get('state')
            country_id = request.POST.get('country')
            images = request.FILES.getlist('images')
            street_address = request.POST.get('street_address')
            postal_code = request.POST.get('postal_code')
            held_date = request.POST.get('held_date')
            held_date = held_date if held_date != '' else None
            
            expiration_date = request.POST.get('expiration_date')
            expiration_date = expiration_date if expiration_date != '' else None
            status = 'Available'  # You can set the status as per your requirement

            # Retrieve or create State, Country, and Category instances
            state = get_object_or_404(State, uuid=state_id)
            country = get_object_or_404(Country, uuid=country_id)
            category = get_object_or_404(FoodSharingCategory, uuid=category_id)

            # # Create SustainableMarketplaceListing instance
            sustainable_listing = FoodSharingListing.objects.create(
                user=user,
                title=title,
                description=description,
                price=price,
                state_id=state,
                country_id=country,
                category_id=category,
                status=status,
                street_address = street_address,
                postal_code = postal_code,
                held_date = held_date,
                expiration_date = expiration_date,
                creator=request.user
            )
            # Add images to the listing
            for image in images:
                sustainable_listing.images.add(FoodSharingListingImage.objects.create(image=image))

            # Return a success response
            messages.success(request, 'Successfully Created Listing')
            return redirect('food_list')
        else:
            form = FoodSharingListingForm(None, request.POST)
    else:
        create_food_form = FoodSharingListingForm()
    return render(request,'food_list.html',{'food_list':food_list,'images': images, 'create_food_form':create_food_form})


def food_detail(request):
    #food_detail = get_object_or_404(FoodSharingListing)
    return render(request,'food_detail.html')

@staff_member_required
def admin_food(request):
    food_data = get_food_data()
    if request.method == 'POST':
        if 'addListing' in request.POST:
            print(request.POST)
            user = request.user  # Assuming user is authenticated
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            category_id = request.POST.get('category')
            state_id = request.POST.get('state')
            country_id = request.POST.get('country')
            images = request.FILES.getlist('images')
            street_address = request.POST.get('street_address')
            postal_code = request.POST.get('postal_code')
            held_date = request.POST.get('held_date')
            held_date = held_date if held_date != '' else None
            
            expiration_date = request.POST.get('expiration_date')
            expiration_date = expiration_date if expiration_date != '' else None
            status = 'Available'  # You can set the status as per your requirement

            # Retrieve or create State, Country, and Category instances
            state = get_object_or_404(State, uuid=state_id)
            country = get_object_or_404(Country, uuid=country_id)
            category = get_object_or_404(FoodSharingCategory, uuid=category_id)

            # # Create SustainableMarketplaceListing instance
            sustainable_listing = FoodSharingListing.objects.create(
                user=user,
                title=title,
                description=description,
                price=price,
                state_id=state,
                country_id=country,
                category_id=category,
                status=status,
                street_address = street_address,
                postal_code = postal_code,
                held_date = held_date,
                expiration_date = expiration_date,
                creator=request.user
            )
            # Add images to the listing
            for image in images:
                sustainable_listing.images.add(FoodSharingListingImage.objects.create(image=image))

            # Return a success response
            messages.success(request, 'Successfully Created Listing')
            return redirect('admin_food')
        elif 'modifyListing' in request.POST:
            food_listing = FoodSharingListing.objects.get(listing_id=request.POST.get('listing_id'))
            print(request.POST.get('title'))
            food_listing.title = request.POST.get('title')
            food_listing.description = request.POST.get('description')
            food_listing.price = request.POST.get('price')
            # Retrieve or create State, Country, and Category instances
            state = get_object_or_404(State, uuid=request.POST.get('state'))
            category = get_object_or_404(FoodSharingCategory, uuid=request.POST.get('category'))
            food_listing.state_id = state
            food_listing.category_id = category
            food_listing.status = request.POST.get('status')
            food_listing.street_address = request.POST.get('street_address')
            food_listing.postal_code = request.POST.get('postal_code')
            held_date = request.POST.get('held_date')
            held_date = held_date if held_date != '' else None
            
            expiration_date = request.POST.get('expiration_date')
            expiration_date = expiration_date if expiration_date != '' else None
            images = request.FILES.getlist('images')
            removed_image_data = request.POST.get('removed-image') 

            # Regular expression to match UUID format
            uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

            # Find all UUIDs in the string
            matches = re.findall(uuid_pattern, removed_image_data)
            with transaction.atomic():
                # Print each extracted UUID
                for uuid in matches:
                    image = FoodSharingListingImage.objects.get(uuid=uuid)
                    image.delete()
                for image in images:
                    food_listing.images.add(FoodSharingListingImage.objects.create(image=image))
                food_listing.save()
            # print(request.POST)
                # Return a success response
            messages.success(request, 'Successfully Modify Listing')
            return redirect('admin_food')
        elif 'deleteListing' in request.POST:
            food_listing = FoodSharingListing.objects.get(listing_id=request.POST.get('listing_id')).delete()
            messages.success(request, 'Listing Deleted')
            return redirect('admin_food')
    return render(request,'admin_food.html',{'food_list':food_data})



def get_food_data():
     # Define a Prefetch object to fetch related images
    image_prefetch = Prefetch('images', queryset=FoodSharingListingImage.objects.all())

    # Annotate the queryset to format the date created
    food_list = FoodSharingListing.objects.filter(Q(deleted=False) | Q(deleted__isnull=True)).annotate(
        state_name=F('state_id__state_name'),
        state_uuid=F('state_id__uuid'),
        # state_id=F('state_id__id'),
        country_name=F('country_id__country_name'),
        country_uuid=F('country_id__uuid'),
        # country_id=F('country_id__id'),
        category_name=F('category_id__category_name'),
        category_uuid=F('category_id__uuid'),
        # category_id=F('category_id__id'),
        date_created_formatted=ExpressionWrapper(
            TruncDate(F('date_created')),
            output_field=DateTimeField()
        ),
        held_date_formatted=ExpressionWrapper(
            TruncDate(F('held_date')),
            output_field=DateTimeField()
        ),
        expiration_date_formatted=ExpressionWrapper(
            TruncDate(F('expiration_date')),
            output_field=DateTimeField()
        ),
        
    ).prefetch_related(image_prefetch).order_by('listing_id')

    # Convert queryset to list of dictionaries with nested state, country, and category data
    food_data = [
        {
            'listing_id':listing.listing_id,
            'title': listing.title,
            'description': listing.description,
            'street_address':listing.street_address,
            'postal_code':listing.postal_code,
            'price': listing.price,
            'held_date':listing.held_date_formatted,
            'expiration_date':listing.expiration_date_formatted,
            'state': {
                'name': listing.state_name,
                'uuid': listing.state_uuid,
                'id': listing.state_id.state_id,
            },
            'country': {
                'name': listing.country_name,
                'uuid': listing.country_uuid,
                'id': listing.country_id.country_id,
            },
            'category': {
                'name': listing.category_name,
                'uuid': listing.category_uuid,
                'id': listing.category_id.category_id,
            },
            'date_created_formatted': listing.date_created_formatted,
            'images': [image.image for image in listing.images.all()],
            'status': listing.status,
        }
        for listing in food_list
    ]
    return food_data

def get_listing_data(request):
    listing_id = request.GET.get('listing_id')
    if listing_id:
        try:
            listing = FoodSharingListing.objects.get(listing_id=listing_id)
            images_data = [{'uuid': str(image.uuid), 'url': image.image.url} for image in listing.images.all()]
            formatted_held_date = listing.held_date.strftime('%Y-%m-%dT%H:%M') if listing.held_date else None
            formatted_expiration_date = listing.expiration_date.strftime('%d %m %Y') if listing.expiration_date else None
            print(images_data)
            print(listing.state_id.uuid)
            listing_data = {
                'listing_id': listing.listing_id,
                'title': listing.title,
                'description': listing.description,
                'street_address':listing.street_address,
                'postal_code':listing.postal_code,
                'price': listing.price,
                'held_date':formatted_held_date,
                'expiration_date':listing.expiration_date,
                'state_id':str(listing.state_id.uuid),
                'country_id':str(listing.country_id.uuid),
                'category_id':str(listing.category_id.uuid),
                'status':listing.status,
                'image':images_data,
                'user':listing.user.id
            }
            return JsonResponse({'listing_data': listing_data})
        except FoodSharingListing.DoesNotExist:
            return JsonResponse({'error': 'Listing not found'}, status=404)
    else:
        return JsonResponse({'error': 'Missing listing_id parameter'}, status=400)
    
def get_categories(request):
    categories = FoodSharingCategory.objects.all().values('category_id', 'category_name', 'uuid')
    return JsonResponse(list(categories), safe=False)