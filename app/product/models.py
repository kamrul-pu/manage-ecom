from django.db import models
from common.models import NameSlugDescriptionBaseModel


class Product(NameSlugDescriptionBaseModel):
    channel = models.ForeignKey(
        "channel.Channel", related_name="products", on_delete=models.CASCADE
    )
    sku = models.CharField(max_length=128, db_index=True)
    barcode = models.CharField(max_length=256, blank=True, db_index=True)
    purchase_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
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

    class Meta:
        unique_together = ["sku", "channel"]
        verbose_name_plural = "local_products"

    def __str__(self):
        return f"{self.name} {self.sku}"
