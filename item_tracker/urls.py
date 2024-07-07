from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from items.views import ItemViewSet, CategoryViewSet, LocationViewSet

# item_tracker/urls.py
router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]