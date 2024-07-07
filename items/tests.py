from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from items.models import Category, Location, Item

class CategoryTests(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'name': 'Test Category',
            'description': 'Test Category Description'
        }

    def test_create_category(self):
        url = reverse('category-list')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Test Category')

    def test_get_categories(self):
        Category.objects.create(name="Category 1", description="Description 1")
        Category.objects.create(name="Category 2", description="Description 2")
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Check 'results' key
        self.assertEqual(response.data['count'], 2)  # Check total count

    # ... [other methods remain the same] ...

class LocationTests(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'name': 'Test Location',
            'description': 'Test Location Description'
        }

    def test_create_location(self):
        url = reverse('location-list')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(Location.objects.get().name, 'Test Location')

    def test_get_locations(self):
        Location.objects.create(name="Location 1", description="Description 1")
        Location.objects.create(name="Location 2", description="Description 2")
        url = reverse('location-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Check 'results' key
        self.assertEqual(response.data['count'], 2)  # Check total count

# Add tests for Item
class ItemTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.location = Location.objects.create(name="Test Location")
        self.valid_payload = {
            'name': 'Test Item',
            'description': 'Test Description',
            'quantity': 1,
            'price': '9.99',
            'category': self.category.id,
            'location': self.location.id,
            'is_available': True
        }

    def test_create_item(self):
        """
        Ensure we can create a new item object.
        """
        url = reverse('item-list')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'Test Item')

    def test_get_items(self):
        """
        Ensure we can get a list of items.
        """
        Item.objects.create(name="Item 1", category=self.category, location=self.location, price='9.99')
        Item.objects.create(name="Item 2", category=self.category, location=self.location, price='19.99')
        url = reverse('item-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_single_item(self):
        """
        Ensure we can get a single item object.
        """
        item = Item.objects.create(name="Test Item", category=self.category, location=self.location, price='9.99')
        url = reverse('item-detail', kwargs={'pk': item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], item.name)

    def test_update_item(self):
        """
        Ensure we can update an item object.
        """
        item = Item.objects.create(name="Old Name", category=self.category, location=self.location, price='9.99')
        url = reverse('item-detail', kwargs={'pk': item.pk})
        data = {'name': 'New Name', 'category': self.category.id, 'location': self.location.id, 'price': '19.99'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get(pk=item.pk).name, 'New Name')

    def test_delete_item(self):
        """
        Ensure we can delete an item object.
        """
        item = Item.objects.create(name="Test Item", category=self.category, location=self.location, price='9.99')
        url = reverse('item-detail', kwargs={'pk': item.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)
