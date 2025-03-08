from django.db import models
from common.models import BaseModelWithUID
from product.models import Product


class RequestStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class Stock(BaseModelWithUID):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="stocks"
    )
    stock_level = models.PositiveIntegerField(default=0)
    in_open = models.PositiveIntegerField(default=0)
    minimum_quantity = models.PositiveIntegerField(default=0)
    location = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Stocks"

    class Action:
        ADDITION = "ADDITION"
        SUBTRACTION = "SUBTRACTION"
        FULL_STOCK = "FULL_STOCK"
        NEW_ORDER_ITEM = "NEW_ORDER_ITEM"
        CANCEL_ORDER_ITEM = "CANCEL_ORDER_ITEM"
        DISPATCH_ORDER_ITEM = "DISPATCH_ORDER_ITEM"
        RETURN = "RETURN"

    def __str__(self):
        return f"{self.pk} {self.product}"


class InventoryRequest(BaseModelWithUID):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="inventory_requests"
    )
    data = models.JSONField()  # sku and quantity
    request_status = models.CharField(
        max_length=36,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING,
    )
    location = models.PositiveIntegerField(null=True, blank=True)
    batch_metadata = models.JSONField(
        null=True, blank=True, default=dict
    )  # box number, shipment details, web
    dispatch_by = models.UUIDField(null=True)
    stock_procced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Inventory Request Stock"
        verbose_name_plural = "Inventory Request Stock"

    def __str__(self):
        return f"{self.pk} {self.stock}"
