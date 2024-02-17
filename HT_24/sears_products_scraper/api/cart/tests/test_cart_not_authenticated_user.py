from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from api.products.tests.products_factories import ProductFactory


class CartNotAuthenticatedUserTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_empty_cart_data(self):
        response = self.client.get(reverse("api:cart:cart"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_add_product_to_cart(self):
        product = ProductFactory()
        response = self.client.post(
            path=reverse("api:cart:cart"),
            data={
                'product_id': product.product_id,
                'quantity': 2,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_get_cart_data(self):
        product_1 = ProductFactory()
        product_2 = ProductFactory()
        self.client.post(
            path=reverse("api:cart:cart"),
            data={
                'product_id': product_1.product_id,
                'quantity': 2,
            }
        )
        self.client.post(
            path=reverse("api:cart:cart"),
            data={
                'product_id': product_2.product_id,
                'quantity': 5,
            }
        )
        response = self.client.get(reverse("api:cart:cart"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_delete_cart_data(self):
        product = ProductFactory()
        self.client.post(
            path=reverse("api:cart:cart"),
            data={
                'product_id': product.product_id,
                'quantity': 2,
            }
        )
        response = self.client.delete(reverse("api:cart:cart"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_clear_empty_cart(self):
        response = self.client.delete(reverse("api:cart:cart"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

class CartUnitNotAuthenticatedUserTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_cart_unit_data(self):
        product = ProductFactory()
        self.client.post(
            path=reverse("api:cart:cart"),
            data={
                'product_id': product.product_id,
                'quantity': 2,
            }
        )
        response = self.client.get(reverse("api:cart:cart_product", kwargs={'product_id': product.product_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_get_not_added_cart_unit_data(self):
        product_id = 'test_product_id'
        response = self.client.get(reverse("api:cart:cart_product", kwargs={'product_id': product_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_update_cart_unit_data(self):
        product = ProductFactory()
        self.client.post(
            path=reverse("api:cart:cart"),
            data={
                'product_id': product.product_id,
                'quantity': 2,
            }
        )
        updated_quantity = 5
        response = self.client.patch(
            path=reverse("api:cart:cart_product", kwargs={'product_id': product.product_id}),
            data={'quantity': updated_quantity},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_update_not_added_cart_unit_data(self):
        product_id = 'test_product_id'
        updated_quantity = 5
        response = self.client.patch(
            path=reverse("api:cart:cart_product", kwargs={'product_id': product_id}),
            data={'quantity': updated_quantity},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_update_chart_unit_data_with_not_positive_integer(self):
        product = ProductFactory()
        self.client.post(
            path=reverse("api:cart:cart"),
            data={
                'product_id': product.product_id,
                'quantity': 2,
            }
        )
        updated_quantity = 0
        response = self.client.patch(
            path=reverse("api:cart:cart_product", kwargs={'product_id': product.product_id}),
            data={'quantity': updated_quantity},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_delete_cart_unit_data(self):
        product = ProductFactory()
        self.client.post(
            path=reverse("api:cart:cart"),
            data={
                'product_id': product.product_id,
                'quantity': 2,
            }
        )
        response = self.client.delete(reverse("api:cart:cart_product", kwargs={'product_id': product.product_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_delete_not_added_cart_unit_data(self):
        product_id = 'test_product_id'
        response = self.client.delete(reverse("api:cart:cart_product", kwargs={'product_id': product_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

