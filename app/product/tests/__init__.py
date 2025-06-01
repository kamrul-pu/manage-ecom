import factory
from factory.django import DjangoModelFactory
from faker import Faker

from product.models import Product, MarketplaceProduct, Mapping
from store.tests import StoreFactory
from core.tests import OrganizationFactory
from store.models import Store
from core.models import Organization
from common.choices import MarketPlace

faker = Faker()


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda o: o.name.lower())
    description = factory.Faker("sentence")
    organization = factory.SubFactory(OrganizationFactory)
    category = factory.Faker("word")
    sku = factory.Faker("ean13")
    barcode = factory.Faker("ean8")
    style = factory.Faker("word")
    color = factory.Faker("color_name")
    purchase_price = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )
    purchase_currency = "USD"
    selling_price = factory.Faker(
        "pydecimal", left_digits=3, right_digits=2, positive=True
    )
    selling_currency = "USD"
    is_composite = False
    is_child = False
    image = factory.Faker("image_url")
    weight = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    height = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    width = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    depth = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    stock_notification = factory.Faker("boolean")
    metadata = {}


class MarketplaceProductFactory(DjangoModelFactory):
    class Meta:
        model = MarketplaceProduct

    name = factory.Faker("word")
    slug = factory.LazyAttribute(lambda o: o.name.lower())
    description = factory.Faker("sentence")
    store = factory.SubFactory(StoreFactory)
    marketplace_id = factory.Faker("uuid4")
    marketplace = factory.Iterator([choice[0] for choice in MarketPlace.choices])
    sku = factory.Faker("ean13")
    category = factory.Faker("word")
    image = factory.Faker("image_url")
    url = factory.Faker("url")
    fbm = factory.Faker("boolean")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    currency = "USD"
    metadata = {}


class MappingFactory(DjangoModelFactory):
    class Meta:
        model = Mapping

    product = factory.SubFactory(ProductFactory)
    marketplace_product = factory.SubFactory(MarketplaceProductFactory)
    store = factory.LazyAttribute(lambda o: o.marketplace_product.store)
    marketplace = factory.LazyAttribute(lambda o: o.marketplace_product.marketplace)
