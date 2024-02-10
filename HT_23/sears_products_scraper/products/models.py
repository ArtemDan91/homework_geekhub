from autoslug import AutoSlugField
from django.db import models


class ScrapedProduct(models.Model):
    product_description_name = models.CharField(max_length=255)
    sell_price = models.FloatField()
    product_id = models.CharField(max_length=50)
    short_description = models.TextField()
    brand_name = models.CharField(max_length=100)
    url = models.URLField()

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    def __str__(self):
        return self.product_description_name


class Category(models.Model):
    name = models.CharField(max_length=255)
    name_slug = AutoSlugField(
        populate_from='name',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class ScrapingTask(models.Model):
    products_ids_list = models.TextField(null=True)
