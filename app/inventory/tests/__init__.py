import factory
from factory.django import DjangoModelFactory
from inventory.models import Stock, InventoryRequest
from product.models import Product
from store.models import Warehouse
from inventory.choices import RequestStatus


class StockFactory(DjangoModelFactory):
    class Meta:
        model = Stock

    product = factory.Iterator(Product.objects.filter())
    sku = factory.LazyAttribute(lambda obj: obj.product.sku if obj.product else "SKU-001")
    warehouse = factory.Iterator(Warehouse.objects.filter()) 
    stock_level = factory.Faker("random_int", min=0, max=500)
    in_open = factory.Faker("random_int", min=0, max=50)
    minimum_quantity = factory.Faker("random_int", min=0, max=10)
    reserve = factory.Faker("random_int", min=0, max=20)


class InventoryRequestFactory(DjangoModelFactory):
    class Meta:
        model = InventoryRequest

    sku = factory.Sequence(lambda n: f"SKU-{n:05}")
    quantity = factory.Faker("random_int", min=1, max=100)
    metadata = factory.LazyAttribute(lambda obj: {"sku": obj.sku, "requested_quantity": obj.quantity})
    request_status = factory.Iterator([RequestStatus.PENDING, RequestStatus.APPROVED, RequestStatus.REJECTED])
    dispatch_by = factory.Faker("name")
    stock_procced_at = factory.Faker("date_time_this_year", before_now=True, after_now=False)
