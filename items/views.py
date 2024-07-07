from rest_framework import viewsets
from .models import Item, Category, Location
from .serializers import ItemSerializer, CategorySerializer, LocationSerializer
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-date_added')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'location', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'date_added']

    def perform_update(self, serializer):
        instance = self.get_object()
        # Delete old image if a new one is uploaded
        if 'image' in self.request.data and instance.image:
            instance.image.delete()
        serializer.save()

    @action(detail=False, methods=['get'])
    def grouped_by_category(self, request):
        queryset = self.get_queryset().values('category__name').annotate(count=Count('id'))
        return Response(queryset)

    @action(detail=False, methods=['get'])
    def grouped_by_location(self, request):
        queryset = self.get_queryset().values('location__name').annotate(count=Count('id'))
        return Response(queryset)
