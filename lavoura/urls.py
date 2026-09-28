from django.urls import include, path
from .views import TalhaoViewSet, LoteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'talhoes', TalhaoViewSet)
router.register(r'lotes', LoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
