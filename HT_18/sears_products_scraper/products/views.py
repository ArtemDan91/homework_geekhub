import subprocess
import sys

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import ScrapedProduct
from .models import ScrapingTask
from .forms import ScrapingTaskForm


def get_all_products(request):
    products = ScrapedProduct.objects.all().order_by('id')
    items_per_page = 20

    paginator = Paginator(products, items_per_page)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'products/all_products.html', {'products': products})


def add_products(request):
    scraper_result_messages = []
    if request.method == 'POST':
        form = ScrapingTaskForm(request.POST)
        if form.is_valid():
            products_ids_list = form.cleaned_data.get('product_id', '')
            for product_id in products_ids_list:
                messages.success(request, f'Product ID {product_id} added successfully')
                task = ScrapingTask(product_id=product_id)
                task.save()

                script_path = str(settings.BASE_DIR / 'scraper_services' / 'products_scraper.py')
                result = subprocess.run(
                    [sys.executable, script_path, product_id], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                scraper_result_message = result.stdout.decode() + result.stderr.decode()
                scraper_result_messages.append((product_id, scraper_result_message))
                print(scraper_result_message)

    else:
        form = ScrapingTaskForm()
    return render(request, 'products/add_products.html', {'form': form, 'scraper_result_messages': scraper_result_messages})


def get_product_data(request, product_id):
    product = get_object_or_404(ScrapedProduct, product_id=product_id)
    return render(request, 'products/product_data.html', {'product': product})