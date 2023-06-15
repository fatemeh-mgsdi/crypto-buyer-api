from django.urls import path, include
from rest_framework import routers
from .views import CryptoViewSet

router = routers.DefaultRouter()
router.register('crypto', CryptoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]