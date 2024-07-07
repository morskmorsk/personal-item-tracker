from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from items.models import Category, Location, Item

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

import tempfile
from PIL import Image

class CategoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
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
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
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

class ItemTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.category = Category.objects.create(name="Test Category")
        self.location = Location.objects.create(name="Test Location")
        self.image = self.create_temporary_image()
        self.valid_payload = {
            'name': 'Test Item',
            'description': 'Test Description',
            'quantity': 1,
            'price': '9.99',
            'category': self.category.id,
            'location': self.location.id,
            'is_available': True
        }
    def create_temporary_image(self):
        # Create a new image file
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, 'jpeg')
        tmp_file.seek(0)
        return tmp_file


    def test_create_item(self):
        """
        Ensure we can create a new item object.
        """
        url = reverse('item-list')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'Test Item')

    def test_create_item_with_image(self):
        url = reverse('item-list')
        data = self.valid_payload.copy()
        data['image'] = self.image
        response = self.client.post(url, data, format='multipart')
        print(response.content)  # Keep this line for debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Item.objects.get().image)

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
