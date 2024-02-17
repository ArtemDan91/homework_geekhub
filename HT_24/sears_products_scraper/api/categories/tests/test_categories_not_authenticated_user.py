from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from api.categories.tests.categories_factories import CategoryFactory


class CategoriesNotAuthenticatedUserTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_empty_categories(self):
        response = self.client.get(reverse("api:categories-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertEqual(response.data['results'], [], msg=response.content)

    def test_list_categories(self):
        categories = CategoryFactory.create_batch(3)
        response = self.client.get(reverse("api:categories-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.content)
        self.assertIn('results', response.data, msg=response.content)
        self.assertEqual(len(response.data['results']), len(categories), msg=response.content)

    def test_get_scraped_category(self):
        categories = CategoryFactory.create_batch(3)
        category_to_retrieve = categories[0]
        response = self.client.get(reverse("api:categories-detail", kwargs={'id': category_to_retrieve.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response)

    def test_add_category(self):
        category = CategoryFactory()
        response = self.client.post(
            path=reverse("api:categories-list"),
            data={
                'name': category.name,
                'name_slug': category.name_slug,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)

    def test_delete_category(self):
        categories = CategoryFactory.create_batch(3)
        category_to_delete = categories[0]
        response = self.client.delete(
            path=reverse("api:categories-detail", kwargs={'id': category_to_delete.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.content)