from django.urls import path

from . import views

app_name = "cart"
urlpatterns = [
    path("", views.checkout_cart, name="checkout_cart"),
    path('update_cart/', views.update_cart_data, name='update_cart_data'),
]