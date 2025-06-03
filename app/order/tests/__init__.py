import factory
from factory import fuzzy
from faker import Faker
from decimal import Decimal
from django.utils import timezone

from order.models import Order, OrderItem, ShippingAddress
from store.models import Store  # adjust the import as per your app layout
from common.choices import MarketPlace
from order.choices import DispatchStatus, PickedItemType, PaymentStatus

fake = Faker()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    store = factory.Iterator(Store().get_all_actives())
    marketplace_order_id = factory.Faker("uuid4")
    payment_status = fuzzy.FuzzyChoice(PaymentStatus.values)
    payment_method = fuzzy.FuzzyChoice(["Credit Card", "PayPal", "Bank Transfer"])
    purchase_date = factory.LazyFunction(timezone.now)
    currency = "USD"
    total = Decimal("0.00")  # Will be updated after items are added
    marketplace = fuzzy.FuzzyChoice(MarketPlace.values)
    dispatch_status = fuzzy.FuzzyChoice(DispatchStatus.values)
    dispatch_identifier = factory.Faker("uuid4")
    dispatched_by = factory.Faker("name")
    dispatched_at = factory.LazyFunction(timezone.now)
    shipped_at = factory.LazyFunction(timezone.now)
    order_meta = factory.LazyFunction(dict)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.Iterator(Order().get_all_actives())
    sku = factory.Faker("ean13")
    local_sku = factory.Faker("ean8")
    quantity = fuzzy.FuzzyInteger(1, 5)
    price = fuzzy.FuzzyDecimal(5.00, 100.00)
    total_amount = factory.LazyAttribute(lambda o: o.quantity * o.price)
    position_item_ids = factory.LazyFunction(lambda: [fake.uuid4() for _ in range(2)])
    picked_sku = factory.Faker("ean13")
    picked_at = factory.LazyFunction(timezone.now)
    picked_item_type = fuzzy.FuzzyChoice(PickedItemType.values)
    packed_sku = factory.Faker("ean13")
    packed_at = factory.LazyFunction(timezone.now)


class ShippingAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShippingAddress

    # order = factory.Iterator(Order().get_all_actives())
    order = factory.SubFactory(OrderFactory)
    buyer_name = factory.Faker("name")
    address1 = factory.Faker("street_address")
    address2 = factory.Faker("secondary_address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    post_code = factory.Faker("postcode")
    country = factory.Faker("country")
    phone = factory.Faker("phone_number")
    reference_id = factory.Faker("uuid4")
    email = factory.Faker("email")
