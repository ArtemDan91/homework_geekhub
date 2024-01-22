import json
import subprocess
import sys

from cart.cart import Cart
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .forms import ScrapingTaskForm
from .forms import EditProductForm
from .models import ScrapedProduct
from .models import Category
from .models import ScrapingTask


def get_all_products(request):
    products = ScrapedProduct.objects.all().order_by('id')
    categories = Category.objects.all()
    items_per_page = 15

    paginator = Paginator(products, items_per_page)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    offset = items_per_page * (products.number - 1)
    return render(request, 'products/all_products.html', {'products': products, 'categories': categories, 'offset': offset})


def get_products_by_categories(request, category_name_slug):
    categories = Category.objects.all()
    product_category = Category.objects.filter(name_slug=category_name_slug).first()
    products_by_categories = ScrapedProduct.objects.filter(category=product_category)
    return render(request, 'products/products_by_categories.html',
                  {'products_by_categories': products_by_categories, 'product_category': product_category, 'categories': categories})


def add_products(request):
    if not request.user.is_superuser:
        return redirect('products:products_table')
    if request.method == 'POST':
        form = ScrapingTaskForm(request.POST)
        if form.is_valid():
            products_ids_list = form.cleaned_data.get('products_ids_list', '')
            serialized_products_ids_list = json.dumps(products_ids_list)
            scraping_task_instance = ScrapingTask(products_ids_list=serialized_products_ids_list)
            scraping_task_instance.save()

            script_path = str(settings.BASE_DIR / 'scraper_services' / 'products_scraper.py')
            subprocess.Popen([sys.executable, script_path, str(scraping_task_instance.id)])
    else:
        form = ScrapingTaskForm()
    return render(request, 'products/add_products.html', {'form': form})


def get_product_data(request, category_name_slug, product_id):
    product = get_object_or_404(ScrapedProduct, product_id=product_id)
    return render(request, 'products/product_data.html', {'product': product})


def edit_product(request, category_name_slug, product_id):
    product = get_object_or_404(ScrapedProduct, product_id=product_id)
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to edit this product.")
        return redirect('products:products_table')
    if request.method == 'POST':
        form = EditProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,f"Product (id {product_id}) changed successfully!")
            return redirect(reverse('products:product_data', args=[category_name_slug, product_id]))
    else:
        form = EditProductForm(instance=product)

    return render(request, 'products/edit_product.html', {'product': product, 'form': form})


def update_product_from_store(request, category_name_slug, product_id):
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to update this product.")
        return redirect('products:products_table')
    serialized_products_ids_list = json.dumps([product_id])
    scraping_task_instance = ScrapingTask(products_ids_list=serialized_products_ids_list)
    scraping_task_instance.save()

    script_path = str(
        settings.BASE_DIR / 'scraper_services' / 'products_scraper.py')
    subprocess.Popen(
        [sys.executable, script_path, str(scraping_task_instance.id)])
    messages.success(request,
                     f"Product (id {product_id}) updating in process... Refresh the site page after a few seconds!")
    return redirect(reverse('products:edit_product', args=[category_name_slug, product_id]))


def delete_product(request, category_name_slug, product_id):
    product = get_object_or_404(ScrapedProduct, product_id=product_id)
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to delete this product.")
        return redirect('products:products_table')

    cart = Cart(request)
    cart.remove_product(product_id)

    product.delete()
    messages.success(request,
                     f"Product (id {product_id}) deleted successfully!")
    return redirect('products:products_table')