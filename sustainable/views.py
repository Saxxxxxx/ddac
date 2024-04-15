from django.shortcuts import render, get_object_or_404,redirect
from .models import SustainableMarketplaceListing,SustainableMarketplaceCategory,SustainableMarketplaceListingImage
from general.models import State,Country
from .forms import SustainableMarketplaceListingForm
from django.db.models import Prefetch, Q, F, ExpressionWrapper, DateTimeField, Count
from django.db.models.functions import Cast
from django.db.models.functions import TruncDate
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.template.loader import render_to_string

import re
# Create your views here.

from django.http import JsonResponse

def filter_view(request):
    data = SustainableMarketplaceListing.objects.all()

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

    return render(request, 'sustainable_list.html', {'data': data, 'selected_category': category, 'selected_location': location, 'selected_status': status})


def sustainable_list(request):
    sustainable_list = SustainableMarketplaceListing.objects.filter(Q(deleted=False) | Q(deleted__isnull=True))
    if request.GET.get('category'):
        category = request.GET.get('category')
        print(category) 
        sustainable_list = sustainable_list.filter(category_id__category_name=category)

    if request.GET.get('location'):
        location = request.GET.get('location')
        sustainable_list = sustainable_list.filter(state_id__state_name=location)
    if request.GET.get('status'):
        status = request.GET.get('status')
        sustainable_list = sustainable_list.filter(status=status)
    print(sustainable_list)
    for listing in sustainable_list:
    # Accessing all images associated with the listing
        images = listing.images.all()
    # Looping through each image
        for image in images:
        # Accessing image attributes
            image_url = image.image
            print(image_url)
        # Do whatever you need with the image_id and image_url
    #NEED TO CHECK IF USER IS LOGIN, IF NOT LOGIN CANT CREATE 
    if request.method == 'POST':
        if 'addListing' in request.POST:
            # create_sustainable_form = SustainableMarketplaceListingForm(request.POST)
            # if create_sustainable_form.is_valid():
            #     # Save the form data
            #     create_sustainable_form.save(commit=False)
            print(request.FILES.getlist('images'))
            user = request.user  # Assuming user is authenticated
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            category_id = request.POST.get('category')
            state_id = request.POST.get('state')
            country_id = request.POST.get('country')
            images = request.FILES.getlist('images')
            status = 'Available'  # You can set the status as per your requirement

            # Retrieve or create State, Country, and Category instances
            state = get_object_or_404(State, uuid=state_id)
            country = get_object_or_404(Country, uuid=country_id)
            category = get_object_or_404(SustainableMarketplaceCategory, uuid=category_id)

            # # Create SustainableMarketplaceListing instance
            sustainable_listing = SustainableMarketplaceListing.objects.create(
                user=user,
                title=title,
                description=description,
                price=price,
                state_id=state,
                country_id=country,
                category_id=category,
                status=status,
                creator=request.user
            )
            # Add images to the listing
            for image in images:
                sustainable_listing.images.add(SustainableMarketplaceListingImage.objects.create(image=image))

            # Return a success response
            messages.success(request, 'Successfully Created Listing')
            return redirect('sustainable_list')
        else:
            create_sustainable_form = SustainableMarketplaceListingForm(None, request.POST)
    else:
        create_sustainable_form = SustainableMarketplaceListingForm()
    return render(request,'sustainable_list.html',{'sustainable_list':sustainable_list,'create_sustainable_form':create_sustainable_form})

def sustainable_detail(request,pk):
    sustainable_list = get_object_or_404(SustainableMarketplaceListing,pk=pk)
    return render(request,'sustainable_detail.html')

@staff_member_required
def admin_sustainable(request):
    sustainable_data = get_sustainable_data()
    if request.method == 'POST':
        if 'addListing' in request.POST:
            print(request.FILES.getlist('images'))
            user = request.user  # Assuming user is authenticated
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            category_id = request.POST.get('category')
            state_id = request.POST.get('state')
            country_id = request.POST.get('country')
            images = request.FILES.getlist('images')
            status = 'Available'  # You can set the status as per your requirement

            # Retrieve or create State, Country, and Category instances
            state = get_object_or_404(State, uuid=state_id)
            country = get_object_or_404(Country, uuid=country_id)
            category = get_object_or_404(SustainableMarketplaceCategory, uuid=category_id)

            # # Create SustainableMarketplaceListing instance
            sustainable_listing = SustainableMarketplaceListing.objects.create(
                user=user,
                title=title,
                description=description,
                price=price,
                state_id=state,
                country_id=country,
                category_id=category,
                status=status,
                creator=request.user
            )
            # Add images to the listing
            for image in images:
                sustainable_listing.images.add(SustainableMarketplaceListingImage.objects.create(image=image))

            # Return a success response
            messages.success(request, 'Successfully Created Listing')
            return redirect('admin_sustainable')
        elif 'modifyListing' in request.POST:
            sustainable_listing = SustainableMarketplaceListing.objects.get(listing_id=request.POST.get('listing_id'))
            print(request.POST.get('title'))
            sustainable_listing.title = request.POST.get('title')
            sustainable_listing.description = request.POST.get('description')
            sustainable_listing.price = request.POST.get('price')
            # Retrieve or create State, Country, and Category instances
            state = get_object_or_404(State, uuid=request.POST.get('state'))
            category = get_object_or_404(SustainableMarketplaceCategory, uuid=request.POST.get('category'))
            sustainable_listing.state_id = state
            sustainable_listing.category_id = category
            sustainable_listing.status = request.POST.get('status')
            images = request.FILES.getlist('images')
            removed_image_data = request.POST.get('removed-image') 

            # Regular expression to match UUID format
            uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

            # Find all UUIDs in the string
            matches = re.findall(uuid_pattern, removed_image_data)
            with transaction.atomic():
                # Print each extracted UUID
                for uuid in matches:
                    image = SustainableMarketplaceListingImage.objects.get(uuid=uuid)
                    image.delete()
                for image in images:
                    sustainable_listing.images.add(SustainableMarketplaceListingImage.objects.create(image=image))
                sustainable_listing.save()
            # print(request.POST)
                # Return a success response
            messages.success(request, 'Successfully Modify Listing')
            return redirect('admin_sustainable')
        elif 'deleteListing' in request.POST:
            sustainable_listing = SustainableMarketplaceListing.objects.get(listing_id=request.POST.get('listing_id')).delete()
            messages.success(request, 'Listing Deleted')
            return redirect('admin_sustainable')
    return render(request, 'admin_sustainable.html', {'sustainable_list': sustainable_data})

def get_sustainable_data():
     # Define a Prefetch object to fetch related images
    image_prefetch = Prefetch('images', queryset=SustainableMarketplaceListingImage.objects.all())

    # Annotate the queryset to format the date created
    sustainable_list = SustainableMarketplaceListing.objects.filter(Q(deleted=False) | Q(deleted__isnull=True)).annotate(
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
        )
    ).prefetch_related(image_prefetch).order_by('listing_id')

    # Convert queryset to list of dictionaries with nested state, country, and category data
    sustainable_data = [
        {
            'listing_id':listing.listing_id,
            'title': listing.title,
            'description': listing.description,
            'price': listing.price,
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
        for listing in sustainable_list
    ]
    return sustainable_data

def get_listing_data(request):
    listing_id = request.GET.get('listing_id')
    if listing_id:
        try:
            listing = SustainableMarketplaceListing.objects.get(listing_id=listing_id)
            images_data = [{'uuid': str(image.uuid), 'url': image.image.url} for image in listing.images.all()]
            print(images_data)
            print(listing.state_id.uuid)
            listing_data = {
                'listing_id': listing.listing_id,
                'title': listing.title,
                'description': listing.description,
                'price': listing.price,  # Convert Decimal to string for JSON serialization
                'state_id':str(listing.state_id.uuid),
                'country_id':str(listing.country_id.uuid),
                'category_id':str(listing.category_id.uuid),
                'status':listing.status,
                'image':images_data,
                'user':listing.user.id
            }
            return JsonResponse({'listing_data': listing_data})
        except SustainableMarketplaceListing.DoesNotExist:
            return JsonResponse({'error': 'Listing not found'}, status=404)
    else:
        return JsonResponse({'error': 'Missing listing_id parameter'}, status=400)

    
def get_categories(request):
    categories = SustainableMarketplaceCategory.objects.all().values('category_id', 'category_name', 'uuid')
    return JsonResponse(list(categories), safe=False)
