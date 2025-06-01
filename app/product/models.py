from django.db import models
from common.models import NameSlugDescriptionBaseModel, BaseModelWithUID
from common.choices import MarketPlace


class Product(NameSlugDescriptionBaseModel):
    organization = models.ForeignKey(
        "core.Organization", related_name="products", on_delete=models.CASCADE
    )
    category = models.TextField(max_length=512, blank=True, null=True)
    sku = models.CharField(max_length=128, db_index=True)
    barcode = models.CharField(max_length=256, blank=True, db_index=True)
    style = models.CharField(max_length=128, blank=True, null=True)
    color = models.CharField(max_length=128, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    purchase_currency = models.CharField(max_length=10, blank=True, default="USD")
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    selling_currency = models.CharField(max_length=10, blank=True, default="USD")
    is_composite = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)
    image = models.URLField(
        max_length=2048, null=True, blank=True
    )  # Changed to URLField
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    height = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    width = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    depth = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_notification = models.BooleanField(default=False)
    metadata = models.JSONField(blank=True, default=dict)

    class Meta:
        verbose_name_plural = "local_products"

    def __str__(self):
        return f"{self.name} {self.sku}"


class MarketplaceProduct(NameSlugDescriptionBaseModel):
    store = models.ForeignKey(
        "store.Store", related_name="marketplace_products", on_delete=models.CASCADE
    )
    marketplace_id = models.CharField(max_length=128, blank=True, db_index=True)
    marketplace = models.CharField(max_length=128, blank=True)
    sku = models.CharField(max_length=128, blank=True, db_index=True)
    category = models.TextField(max_length=512, blank=True, null=True)
    image = models.URLField(max_length=2048, null=True, blank=True)
    url = models.URLField(max_length=2048, null=True, blank=True)
    # fbm => Fulfilled By Marketplace
    fbm = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=10, blank=True, default="USD")
    metadata = models.JSONField(blank=True, default=dict)

    class Meta:
        verbose_name_plural = "marketplace_products"

    def __str__(self):
        return f"{self.name} {self.sku}"


class Mapping(BaseModelWithUID):
    product = models.ForeignKey(
        Product, related_name="mappings", on_delete=models.CASCADE
    )
    marketplace_product = models.ForeignKey(
        MarketplaceProduct, related_name="mappings", on_delete=models.CASCADE
    )
    store = models.ForeignKey(
        "store.Store", related_name="mappings", on_delete=models.CASCADE
    )
    marketplace = models.CharField(max_length=128, choices=MarketPlace.choices)

    class Meta:
        unique_together = ["product", "marketplace_product", "store"]
        verbose_name_plural = "mappings"

    def __str__(self):
        return (
            f"{self.product.name} - {self.marketplace_product.name} ({self.store.name})"
        )
