from django.urls import path

from . import views

app_name = "cart"
urlpatterns = [
    path("", views.checkout_cart, name="checkout_cart"),
    path('add_cart/', views.add_cart_data, name='add_cart_data'),
    path('change_product_quantity/', views.change_product_quantity, name='change_product_quantity'),
    path('remove_cart_product/', views.remove_cart_product, name='remove_cart_product'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
]