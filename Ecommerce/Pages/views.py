from django.shortcuts import render
from Products.models import Product
# Create your views here.

def home(request):
    products = Product.objects.order_by()[:8]
    return render(request, 'pages/home.html', {'products':products})
def contact_us(request):
    return render(request, 'pages/contact_us.html')
def about(request):
    return render(request, 'pages/about.html')