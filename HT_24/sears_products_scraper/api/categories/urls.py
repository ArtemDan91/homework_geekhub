from rest_framework.routers import SimpleRouter

from api.categories.views import CategoryViewSet

router = SimpleRouter()
router.register('', CategoryViewSet, basename='categories')

urlpatterns = [

]

urlpatterns += router.urls
