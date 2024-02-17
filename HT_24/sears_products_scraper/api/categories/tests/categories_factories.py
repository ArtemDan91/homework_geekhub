import factory

from products.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    name_slug = factory.Faker("slug")

    class Meta:
        model = Category