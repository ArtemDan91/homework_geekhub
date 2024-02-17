from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from api.products.tests.products_factories import ProductFactory


class CartAuthenticatedUserTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test')
        self.client.force_login(self.user)

    def test_get_empty_cart_data(self):
        response = self.client.get(reverse("api:cart:cart"))
        expected_data = {
            'cart_products': [],
            'cart_total_amount': 0,
            'cart_size': 0,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertEqual(response.data, expected_data, msg=response.content)

    def test_add_product_to_cart(self):
        product = ProductFactory()
        response = self.client.post(
            path=reverse("api:cart:cart"),
            data={
                'product_id': product.product_id,
                'quantity': 2,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertEqual(response.data['product_id'], product.product_id, msg=response.content)

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
        expected_data = {
            'cart_products': [
                {
                    'product_id': product_1.product_id,
                    'product_description_name': product_1.product_description_name,
                    'sell_price': product_1.sell_price,
                    'quantity': 2,
                    'products_total_cost': round(product_1.sell_price * 2, 2),
                },
                {
                    'product_id': product_2.product_id,
                    'product_description_name': product_2.product_description_name,
                    'sell_price': product_2.sell_price,
                    'quantity': 5,
                    'products_total_cost': round(product_2.sell_price * 5, 2),
                }
            ],
            'cart_total_amount': round(product_1.sell_price * 2 + product_2.sell_price * 5, 2),
            'cart_size': 7,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertEqual(response.data, expected_data, msg=response.content)

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
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.content)

    def test_clear_empty_cart(self):
        response = self.client.delete(reverse("api:cart:cart"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)
        self.assertEqual(response.json()['error'], 'The cart is already empty', msg=response.content)


class CartUnitAuthenticatedUserTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test')
        self.client.force_login(self.user)

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
        expected_data = {
            'product_id': product.product_id,
            'product_description_name': product.product_description_name,
            'sell_price': product.sell_price,
            'quantity': 2,
            'products_total_cost': round(product.sell_price * 2, 2),
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertEqual(response.data, expected_data, msg=response.content)

    def test_get_not_added_cart_unit_data(self):
        product_id = 'test_product_id'
        response = self.client.get(reverse("api:cart:cart_product", kwargs={'product_id': product_id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)
        self.assertEqual(response.json()['error'], 'This product has not been added to the cart yet', msg=response.content)

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
        self.client.patch(
            path=reverse("api:cart:cart_product", kwargs={'product_id': product.product_id}),
            data={'quantity': updated_quantity},
            format='json'
        )
        expected_data = {
            'product_id': product.product_id,
            'product_description_name': product.product_description_name,
            'sell_price': product.sell_price,
            'quantity': updated_quantity,
            'products_total_cost': round(product.sell_price * updated_quantity, 2),
        }
        response = self.client.get(reverse("api:cart:cart_product", kwargs={'product_id': product.product_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertEqual(response.data, expected_data, msg=response.content)

    def test_update_not_added_cart_unit_data(self):
        product_id = 'test_product_id'
        updated_quantity = 5
        response = self.client.patch(
            path=reverse("api:cart:cart_product", kwargs={'product_id': product_id}),
            data={'quantity': updated_quantity},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)
        self.assertEqual(response.json()['error'], 'This product has not been added to the cart yet',
                         msg=response.content)

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
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)
        self.assertIn('Quantity must be a positive integer', response.json()['error']['quantity'], msg=response.content)

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
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.content)

    def test_delete_not_added_cart_unit_data(self):
        product_id = 'test_product_id'
        response = self.client.delete(reverse("api:cart:cart_product", kwargs={'product_id': product_id}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.content)
        self.assertEqual(response.json()['error'], 'This product has not been added to the cart yet',
                         msg=response.content)