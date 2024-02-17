from itertools import count

import factory

from api.categories.tests.categories_factories import CategoryFactory
from products.models import ScrapedProduct

product_id_generator = count(1)

class ProductFactory(factory.django.DjangoModelFactory):
    product_description_name = factory.Faker('name')
    sell_price = factory.Faker('pyfloat', min_value=0, max_value=1000, right_digits=2)
    product_id = factory.Sequence(lambda n: f'test_product_{n}')
    short_description = factory.Faker('text', max_nb_chars=100)
    brand_name = factory.Faker('name')
    url = factory.Faker('url')
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = ScrapedProduct

