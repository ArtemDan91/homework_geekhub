from django.db import models


class ScrapedProduct(models.Model):
    product_description_name = models.CharField(max_length=255)
    sell_price = models.CharField(max_length=50)
    product_id = models.CharField(max_length=50)
    short_description = models.TextField()
    brand_name = models.CharField(max_length=100)
    category_name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.product_description_name


class ScrapingTask(models.Model):
    products_ids_list = models.TextField(null=True)
