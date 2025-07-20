# your_app_name/views.py

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Product, Category # Make sure to import your Category model
from django.db.models import Q

def category(request, categ):
    categ = categ.replace('-', ' ')
    try:
        category = Category.objects.get(name=categ)
        products = Product.objects.filter(category=category)
        context = {'products':products, 'category':category}
        return render(request, 'products/product_listing_page.html', context)
    except Category.DoesNotExist:
        messages.success(request, ("That Category Doesn't Exist..."))
        return redirect('product_listing_page')

def product_listing_page(request):
    query = request.GET.get('q')
    if query:
        # 1) Apply text filter
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        # 2) Apply category filter if selected
        selected_categories = request.GET.getlist('category')
        if selected_categories:
            products = products.filter(category__name__in=selected_categories)

        # 3) Paginate just as in else:
        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # 4) Only include categories present in the filtered search results:
        cat_ids = products.values_list('category_id', flat=True)
        all_categories = Category.objects.filter(
            id__in=cat_ids
        ).order_by('name')

        # 5) Final context
        context = {
            'page_obj': page_obj,
            'categories': all_categories,
            'selected_categories': selected_categories,
        }

    else:
        product_all = Product.objects.all().order_by('name')
        selected_categories = request.GET.getlist('category')

        if selected_categories:
            product_all = product_all.filter(category__name__in=selected_categories)

        paginator = Paginator(product_all, 6)
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        all_categories = Category.objects.all().order_by('name')

        context = {
            'page_obj': page_obj,
            'categories': all_categories,
            'selected_categories': selected_categories,
            # Remove 'query_params': request.GET.copy(), if you are only using query_string_exclude
        }
    return render(request, 'products/product_listing_page.html', context)
def product_detail_page(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'products/product_detail_page.html', {'product':product})
def search(request):
    return render(request, 'products/search.html')