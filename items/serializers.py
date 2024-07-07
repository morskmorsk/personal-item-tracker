from rest_framework import serializers
from .models import Item, Category, Location

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'quantity', 'date_added', 'price', 'category', 'location', 'is_available', 'image', 'barcode']

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value

    def validate_price(self, value):
        if value and value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description',]

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','name','description',]
