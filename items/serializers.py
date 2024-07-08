# from rest_framework import serializers
# from .models import Item, Category, Location

# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = ['id', 'name', 'description', 'quantity', 'date_added', 'price', 'category', 'location', 'is_available', 'image', 'barcode']

#     def validate_quantity(self, value):
#         if value < 0:
#             raise serializers.ValidationError("Quantity cannot be negative.")
#         return value

#     def validate_price(self, value):
#         if value and value < 0:
#             raise serializers.ValidationError("Price cannot be negative.")
#         return value
from rest_framework import serializers
from .models import Item, Category, Location

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'quantity', 'date_added', 'price', 'category', 'location', 'is_available', 'image', 'barcode']

    def validate(self, data):
        # If we're creating a new item or updating the name, check for duplicates
        if self.instance is None or 'name' in data:
            name = data.get('name', self.instance.name if self.instance else None)
            if Item.objects.filter(name=name).exclude(id=getattr(self.instance, 'id', None)).exists():
                raise serializers.ValidationError("An item with this name already exists.")
        return data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description',]

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','name','description',]
