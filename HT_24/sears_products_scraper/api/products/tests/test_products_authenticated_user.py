from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from api.products.tests.products_factories import ProductFactory


class ScrapedProductAuthenticatedUserTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test')
        self.client.force_login(self.user)

    def test_list_empty_scraped_products(self):
        response = self.client.get(reverse("api:products-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertEqual(response.data['results'], [], msg=response.content)

    def test_list_scraped_products(self):
        products = ProductFactory.create_batch(3)
        response = self.client.get(reverse("api:products-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertIn('results', response.data, msg=response.content)
        self.assertEqual(len(response.data['results']), len(products), msg=response.content)

    def test_get_scraped_product(self):
        products = ProductFactory.create_batch(3)
        product_to_retrieve = products[0]
        response = self.client.get(reverse("api:products-detail", kwargs={'product_id': product_to_retrieve.product_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response)

    def test_add_scraped_product(self):
        product = ProductFactory()
        response = self.client.post(
            path=reverse("api:products-list"),
            data={
                'product_description_name': product.product_description_name,
                'sell_price': product.sell_price,
                'product_id': product.product_id,
                'short_description': product.short_description,
                'brand_name': product.brand_name,
                'url': product.url,
                'category': product.category,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_delete_scraped_product(self):
        products = ProductFactory.create_batch(3)
        product_to_delete = products[0]
        response = self.client.delete(
            path=reverse("api:products-detail", kwargs={'product_id': product_to_delete.product_id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)