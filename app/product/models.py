from django.db import models
from common.models import NameSlugDescriptionBaseModel


class LocalProduct(NameSlugDescriptionBaseModel):
    channel = models.ForeignKey(
        "channel.Channel", related_name="channel_products", on_delete=models.CASCADE
    )
    sku = models.CharField(max_length=128)
    barcode = models.CharField(max_length=256, blank=True)
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


class RemoteProduct(NameSlugDescriptionBaseModel):  # Fixed naming
    local_product = models.ForeignKey(
        LocalProduct, related_name="remote_products", on_delete=models.CASCADE
    )
    channel = models.ForeignKey(
        "channel.Channel",
        related_name="channel_remote_products",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    sku = models.CharField(max_length=128)  # Added explicit SKU field
    image = models.URLField(
        max_length=2048, null=True, blank=True
    )  # Changed to URLField
    fba_status = models.BooleanField(default=False)
    sync_inventory = models.BooleanField(default=True)

    class Meta:
        unique_together = ["sku", "local_product"]  # Fixed unique_together
        verbose_name_plural = "remote_products"

    def __str__(self):
        return f"{self.name} {self.sku}"
