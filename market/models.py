from django.db import models
from django.db.models import TextChoices


class CategoryChoice(TextChoices):
    CPU = 'CPU', 'Processor'
    GPU = 'GPU', 'Graphics Card'
    MONITOR = 'MONITOR', 'Monitor'
    MOTHERBOARD = 'MOTHERBOARD', 'Motherboard'
    OTHER = 'OTHER', 'Other'


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Name')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Description')
    image = models.URLField(blank=True, verbose_name='Image URL')
    category = models.CharField(
        max_length=20, choices=CategoryChoice.choices, default=CategoryChoice.OTHER, verbose_name='Category'
    )
    quantity = models.IntegerField(null=False, blank=False, verbose_name='Quantity')
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, verbose_name='Price')

    def __str__(self):
        return self.name
