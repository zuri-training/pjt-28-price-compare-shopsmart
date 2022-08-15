from django.shortcuts import render

# Create your views here.
def laptop(request):
    return render(request, 'categories/laptop.html')
def mobile(request):
    return render(request, 'categories/mobile.html')