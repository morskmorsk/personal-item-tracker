from rest_framework import viewsets
from .models import Item, Category, Location
from .serializers import ItemSerializer, CategorySerializer, LocationSerializer

# items/views.py
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-date_added')
    serializer_class = ItemSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
