from django.contrib import admin

from .models import ScrapedProduct, ScrapingTask


class ScrapedProductAdmin(admin.ModelAdmin):
    list_display = ["product_description_name", "sell_price", "product_id",
                    "short_description", "brand_name", "category_name", "url"]


class ScrapingTaskAdmin(admin.ModelAdmin):
    list_display = ["id", "products_ids_list"]


# Register your models here.
admin.site.register(ScrapedProduct, ScrapedProductAdmin)
admin.site.register(ScrapingTask, ScrapingTaskAdmin)
