from django.shortcuts import render, redirect
from Cart.cart import Cart
from decimal import Decimal
from Payment.forms import ShippingForm, PaymentForm
from Payment.models import ShippingAddress, Order, OrderItems
from django.contrib import messages
from django.contrib.auth.models import User
from Products.models import Product

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        grand_total = totals + Decimal("10.00")
        if totals == 0:
            grand_total = 0
    # --- Add this new logic ---
        products_with_line_totals = []
        for product in cart_products:
            quantity = quantities.get(str(product.id), 0)
            try:
                product_price = Decimal(str(product.price))
            except (TypeError, ValueError):
                product_price = Decimal('0.00')

            line_total = product_price * quantity
            
            products_with_line_totals.append({
                'product': product,
                'quantity': quantity,
                'line_total': line_total
            })
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        # --- End of new logic ---
        if request.user.is_authenticated:
            return render(request, "payment/billing_info.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'grand_total':grand_total, 'products_with_line_totals':products_with_line_totals, "form": PaymentForm()})
        else:
            return render(request, "payment/billing_info.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_info':request.POST, 'grand_total':grand_total, 'products_with_line_totals':products_with_line_totals, "form": PaymentForm()})
        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'shipping_form':shipping_form, 'grand_total':grand_total, 'products_with_line_totals':products_with_line_totals})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    grand_total = totals + Decimal("10.00")
    if totals == 0:
        grand_total = 0
   # --- Add this new logic ---
    products_with_line_totals = []
    for product in cart_products:
        quantity = quantities.get(str(product.id), 0)
        try:
            product_price = Decimal(str(product.price))
        except (TypeError, ValueError):
            product_price = Decimal('0.00')

        line_total = product_price * quantity
        
        products_with_line_totals.append({
            'product': product,
            'quantity': quantity,
            'line_total': line_total
        })
    # --- End of new logic ---
    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = ShippingAddress.objects.create(id=request.user.id,user=request.user,)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'grand_total':grand_total, 'products_with_line_totals': products_with_line_totals, 'shipping_form':shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {'cart_products':cart_products, 'quantities':quantities, 'totals':totals, 'grand_total':grand_total, 'products_with_line_totals': products_with_line_totals, 'shipping_form':shipping_form})
    

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        grand_total = totals + Decimal("10.00")
        if totals == 0:
            grand_total = 0
    # --- Add this new logic ---
        products_with_line_totals = []
        for product in cart_products:
            quantity = quantities.get(str(product.id), 0)
            try:
                product_price = Decimal(str(product.price))
            except (TypeError, ValueError):
                product_price = Decimal('0.00')

            line_total = product_price * quantity
            
            products_with_line_totals.append({
                'product': product,
                'quantity': quantity,
                'line_total': line_total
            })
        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = grand_total
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id
                price = product.price
                for key,value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItems(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price,)
                        create_order_item.save()
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            messages.success(request, 'Order placed!')
            return redirect('home')
        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk
            for product in cart_products:
                product_id = product.id
                price = product.price
                for key,value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItems(order_id=order_id, product_id=product_id, quantity=value, price=price,)
                        create_order_item.save()
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            
            messages.success(request, 'Order placed!')
            return redirect('home')
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')
    return render(request, "payment/process_order.html", {})
def payment_success(request):

    return render(request, "payment/payment_success.html", {})