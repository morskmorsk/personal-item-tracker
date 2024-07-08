# items/models.py
import os
from django.db import models
from django.utils.text import slugify

# Define the path to upload the item images
def item_image_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Create a slug from the item name
    slug = slugify(instance.name)
    # Return the new path
    return f'item_images/{slug}.{ext}'


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']  # Add this line

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']  # Add this line

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to=item_image_path, null=True, blank=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.image:
            # If an image already exists, delete it
            try:
                this = Item.objects.get(id=self.id)
                if this.image != self.image:
                    this.image.delete(save=False)
            except:
                pass  # when new photo then we do nothing, normal case
        super(Item, self).save(*args, **kwargs)
