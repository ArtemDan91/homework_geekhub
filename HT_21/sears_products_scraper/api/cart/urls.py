from django.urls import path

from api.cart.views import CartView
from api.cart.views import CartProductView

app_name = "cart"

urlpatterns = [
    path('', CartView.as_view(), name="cart"),
    path('<str:product_id>/', CartProductView.as_view(), name="cart_product"),
]

