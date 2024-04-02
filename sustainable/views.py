from django.shortcuts import render, get_object_or_404,redirect
from .models import SustainableMarketplaceListing,SustainableMarketplaceCategory
from .forms import SustainableMarketplaceListingForm
from django.db.models import Q

# Create your views here.

def sustainable_list(request):
    sustainable_list = SustainableMarketplaceListing.objects.filter(Q(deleted=False) | Q(deleted__isnull=True))
    print(sustainable_list)
    #NEED TO CHECK IF USER IS LOGIN, IF NOT LOGIN CANT CREATE 
    if request.method == 'POST':
        if 'createSustainableFormButton' in request.POST:
            create_sustainable_form = SustainableMarketplaceListingForm(request.POST)
            if create_sustainable_form.is_valid():
                # Save the form data
                create_sustainable_form.save(commit=False)
        else:
            create_sustainable_form = SustainableMarketplaceListingForm(None, request.POST)
    else:
        create_sustainable_form = SustainableMarketplaceListingForm()
    return render(request,'sustainable_list.html',{'sustainable_list':sustainable_list,'create_sustainable_form':create_sustainable_form})

def sustainable_detail(request,pk):
    sustainable_list = get_object_or_404(SustainableMarketplaceListing,pk=pk)
    return render(request,'sustainable_detail.html')