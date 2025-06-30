from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from Products.models import Product
from django.http import JsonResponse
from decimal import Decimal
from django.contrib import messages
# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    grand_total = totals + Decimal("10.00")
    if totals == 0:
        grand_total = 0
    return render(request, 'cart/cart_summary.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'grand_total':grand_total})
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added To Cart..."))
        return response 
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        messages.success(request, ("Item Deleted From Shopping Cart..."))
    # return redirect('cart_summary')
    return response
    return render(request, 'cart/cart_delete.html', {})
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty':product_qty})
        messages.success(request, ("Your Car Has Been Updated ..."))
    # return redirect('cart_summary')
    return response