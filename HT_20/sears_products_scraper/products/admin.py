from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import ScrapedProduct, ScrapingTask, Category


class ScrapedProductAdmin(admin.ModelAdmin):
    list_display = ["product_description_name", "sell_price", "product_id",
                    "short_description", "brand_name", "url", "category"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "name_slug"]


class ScrapingTaskAdmin(admin.ModelAdmin):
    list_display = ["id", "products_ids_list"]


class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)
admin.site.register(ScrapedProduct, ScrapedProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ScrapingTask, ScrapingTaskAdmin)
