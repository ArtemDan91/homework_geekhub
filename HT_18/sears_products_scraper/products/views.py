import json
import subprocess
import sys

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import ScrapedProduct
from .models import ScrapingTask
from .forms import ScrapingTaskForm


def get_all_products(request):
    products = ScrapedProduct.objects.all().order_by('id')
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

    return render(request, 'products/all_products.html', {'products': products, 'offset': offset})


def add_products(request):
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


def get_product_data(request, product_id):
    product = get_object_or_404(ScrapedProduct, product_id=product_id)
    return render(request, 'products/product_data.html', {'product': product})