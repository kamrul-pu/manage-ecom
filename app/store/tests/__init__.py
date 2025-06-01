import factory
from factory.django import DjangoModelFactory
from faker import Faker

from store.models import Store, Warehouse
from core.models import Organization
from common.choices import MarketPlace
from store.choices import AuthType, StoreStatus

from core.tests import OrganizationFactory  # assumes you have this already

fake = Faker()


class StoreFactory(DjangoModelFactory):
    class Meta:
        model = Store

    organization = factory.SubFactory(OrganizationFactory)
    name = factory.Faker("company")
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(" ", "-"))
    description = factory.Faker("sentence")

    auth_type = factory.Iterator(AuthType.values)
    store_type = factory.Iterator(["retail", "online", "wholesale"])
    store_status = factory.Iterator(StoreStatus.values)
    marketplace = factory.Iterator(MarketPlace.values)

    shop_url = factory.Faker("url")
    country = factory.Faker("country")
    max_stock = factory.Faker("random_int", min=0, max=500)
    report_ref = factory.LazyFunction(dict)
    report_sorted_by = factory.Faker("word")
    is_authorized = True
    expires_on = factory.Faker("future_datetime")

    access_token = factory.Faker("uuid4")
    refresh_token = factory.Faker("uuid4")
    access_token_expiry = factory.Faker("random_number", digits=10)
    refresh_token_expiry = factory.Faker("random_number", digits=10)
    metadata = factory.LazyFunction(dict)
    order_sync = factory.Faker("boolean")
    inventory_sync = factory.Faker("boolean")


class WarehouseFactory(DjangoModelFactory):
    class Meta:
        model = Warehouse

    store = factory.SubFactory(StoreFactory)
    name = factory.Faker("company")
    slug = factory.LazyAttribute(lambda obj: obj.name.lower().replace(" ", "-"))
    description = factory.Faker("sentence")

    code = factory.Sequence(lambda n: f"WH-{n:04d}")
    address_line1 = factory.Faker("street_address")
    address_line2 = factory.Faker("secondary_address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    postal_code = factory.Faker("postcode")
    country = factory.Faker("country")
    contact_name = factory.Faker("name")
    contact_phone = factory.Faker("phone_number")
    is_primary = factory.Faker("boolean")
    is_active = True
