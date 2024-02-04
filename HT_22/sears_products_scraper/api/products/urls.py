from rest_framework.routers import SimpleRouter

from api.products.views import ScrapedProductViewSet

router = SimpleRouter()
router.register('', ScrapedProductViewSet, basename='products')

urlpatterns = [

]

urlpatterns += router.urls
