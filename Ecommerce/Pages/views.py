from django.shortcuts import render
from Products.models import Product
from django.db.models import Q
# Create your views here.

def home(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.order_by()[:8]
    return render(request, 'pages/home.html', {'products':products})
def contact_us(request):
    return render(request, 'pages/contact_us.html', {'show_aside': True})
def about(request):
    return render(request, 'pages/about.html', {'show_aside': True})