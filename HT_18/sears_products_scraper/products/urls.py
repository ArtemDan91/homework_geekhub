from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("", views.get_all_products, name="products_table"),
    path("add/", views.add_products, name="add_products"),
    path("<slug:product_id>", views.get_product_data, name="product_data"),
]