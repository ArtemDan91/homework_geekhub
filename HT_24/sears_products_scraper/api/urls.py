from django.urls import path
from django.urls import include


app_name = "api"

urlpatterns = [
    path("products/", include("api.products.urls")),
    path("categories/", include("api.categories.urls")),
    path("cart/", include("api.cart.urls")),
]
