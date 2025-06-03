from django.db import models
from common.models import BaseModelWithUID
from product.models import Product

from inventory.choices import RequestStatus


class Stock(BaseModelWithUID):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stocks"
    )
    sku = models.CharField(max_length=100, blank=True)
    warehouse = models.ForeignKey(
        "store.Warehouse",
        on_delete=models.CASCADE,
        related_name="stocks",
        blank=True,
        null=True,
    )
    stock_level = models.PositiveIntegerField(default=0)
    in_open = models.PositiveIntegerField(default=0)
    available = models.PositiveIntegerField(default=0)
    minimum_quantity = models.PositiveIntegerField(default=0)
    reserve = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.pk} {self.sku} - {self.stock_level}"


class InventoryRequest(BaseModelWithUID):
    sku = models.CharField(max_length=100, db_index=True)
    quantity = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(blank=True, default=dict)  # sku and quantity
    request_status = models.CharField(
        max_length=36,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING,
    )
    dispatch_by = models.CharField(max_length=100, blank=True)
    stock_procced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Inventory Request"
        verbose_name_plural = "Inventory Requests"

    def __str__(self):
        return f"{self.pk} {self.sku}"
