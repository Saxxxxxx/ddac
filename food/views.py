from django.shortcuts import render, get_object_or_404,redirect
from .models import FoodSharingListing,FoodSharingCategory
from .forms import FoodSharingListingForm
from django.db.models import Q

# Create your views here.
def food_list(request):
    food_list = FoodSharingListing.objects.filter(Q(deleted=False) | Q(deleted__isnull=True))
    print(food_list)
    create_food_form = ''
    #NEED TO CHECK IF USER IS LOGIN, IF NOT LOGIN CANT CREATE 
    if request.method == 'POST':
        if 'createFoodFormButton' in request.POST:
            create_food_form = FoodSharingListingForm(request.POST)
            if create_food_form.is_valid():
                # Save the form data
                create_food_form.save(commit=False)
        else:
            form = FoodSharingListingForm(None, request.POST)
    else:
        create_food_form = FoodSharingListingForm()
    return render(request,'food_list.html',{'food_list':food_list,'create_food_form':create_food_form})


def food_detail(request,pk):
    food_detail = get_object_or_404(FoodSharingListing,pk=pk)
    return render(request,'')
