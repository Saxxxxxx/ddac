from django.shortcuts import render

# Create your views here.
def education_list(request):
    return render(request,'education_list.html')