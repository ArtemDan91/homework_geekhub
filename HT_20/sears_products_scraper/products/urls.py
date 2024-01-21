from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("", views.get_all_products, name="products_table"),
    path("add/", views.add_products, name="add_products"),
    path("<slug:category_name_slug>/", views.get_products_by_categories, name="products_by_categories_table"),
    path("<slug:category_name_slug>/<str:product_id>/", views.get_product_data, name="product_data"),
    path("<slug:category_name_slug>/edit/<str:product_id>/", views.edit_product, name="edit_product"),
    path("<slug:category_name_slug>/delete/<str:product_id>/", views.delete_product, name="delete_product"),
    path("<slug:category_name_slug>/update/<str:product_id>/", views.update_product_from_store, name="update_product"),
]