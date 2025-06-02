from django.db import models

from common.choices import MarketPlace
from common.models import BaseModelWithUID

from order.choices import DispatchStatus, PickedItemType, PaymentStatus


class Order(BaseModelWithUID):
    store = models.ForeignKey(
        "store.Store",
        related_name="orders",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The sales channel this order originates from.",
    )
    marketplace_order_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique order ID from the Store.",
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text="Current payment status of the order.",
    )
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        help_text="Method used for payment (e.g., Credit Card, PayPal).",
    )
    purchase_date = models.DateTimeField(
        help_text="Date and time the order was placed."
    )
    currency = models.CharField(
        max_length=20,
        blank=True,
        default="USD",
        help_text="Currency code (e.g., USD, EUR).",
    )
    total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, help_text="Total order amount."
    )
    marketplace = models.CharField(
        max_length=50,
        choices=MarketPlace.choices,
        blank=True,
        default=MarketPlace.OTHER,
        db_index=True,
        help_text="Marketplace name (e.g., Amazon, eBay).",
    )
    dispatch_status = models.CharField(
        max_length=20,
        choices=DispatchStatus.choices,
        default=DispatchStatus.OPEN_ORDER,
        help_text="Current dispatch status of the order.",
    )
    dispatch_identifier = models.CharField(
        max_length=128, blank=True, help_text="Identifier for dispatch tracking."
    )
    dispatched_by = models.CharField(
        max_length=128,
        blank=True,
        help_text="Entity or person who dispatched the order.",
    )
    dispatched_at = models.DateTimeField(
        blank=True, null=True, help_text="Date and time of dispatch."
    )
    shipped_at = models.DateTimeField(
        blank=True, null=True, help_text="Date and time of shipment."
    )
    order_meta = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        help_text="Additional metadata for the order.",
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self) -> str:
        return f"{self.marketplace} - {self.marketplace_order_id}"

    def get_order_items_sku_list(self):
        """Return a list of remote SKUs for order items."""
        return list(self.order_items.values_list("sku", flat=True))

    def get_order_item_sku_quantity(self):
        """Return a list of dictionaries with SKU, quantity, and UIDs."""
        return list(self.order_items.values("sku", "quantity", "channel"))


class OrderItem(BaseModelWithUID):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
        help_text="The order this item belongs to.",
    )
    sku = models.CharField(
        max_length=128, blank=True, null=True, help_text="SKU from the channel."
    )
    local_sku = models.CharField(max_length=128, blank=True)
    quantity = models.PositiveIntegerField(
        default=1, help_text="Number of items ordered."
    )
    price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, help_text="Price per unit."
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text="Total price for this item (price * quantity).",
    )
    position_item_ids = models.JSONField(
        blank=True,
        null=True,
        default=list,
        help_text="List of position item IDs (replaced ArrayField for portability).",
    )
    picked_sku = models.CharField(
        max_length=128, blank=True, help_text="SKU of the picked item."
    )
    picked_at = models.DateTimeField(
        blank=True, null=True, help_text="Date and time the item was picked."
    )
    picked_item_type = models.CharField(
        max_length=20,
        choices=PickedItemType.choices,
        blank=True,
        help_text="Type of picked item.",
    )
    packed_sku = models.CharField(
        max_length=128, blank=True, help_text="SKU of the packed item."
    )
    packed_at = models.DateTimeField(
        blank=True, null=True, help_text="Date and time the item was packed."
    )

    class Meta:
        indexes = [
            models.Index(fields=["sku", "order_id"]),
            # models.Index(fields=["channel_uid", "company_uid"]),
        ]
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self) -> str:
        return f"{self.sku} - {self.quantity} pcs"

    def save(self, *args, **kwargs):
        """Automatically calculate total_amount if not provided."""
        if self.price is not None and self.quantity is not None:
            self.total_amount = self.price * self.quantity
        super().save(*args, **kwargs)


class ShippingAddress(BaseModelWithUID):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="shipping_address",
        help_text="The order this shipping address belongs to.",
    )
    buyer_name = models.CharField(
        max_length=255, blank=True, help_text="Name of the buyer."
    )
    address1 = models.CharField(
        max_length=255, blank=True, help_text="Primary address line."
    )
    address2 = models.CharField(
        max_length=255, blank=True, help_text="Secondary address line."
    )
    city = models.CharField(
        max_length=100, blank=True, help_text="City of the shipping address."
    )
    state = models.CharField(max_length=100, blank=True, help_text="State or province.")
    post_code = models.CharField(
        max_length=20, blank=True, help_text="Postal/ZIP code."
    )
    country = models.CharField(
        max_length=100, blank=True, help_text="Country of the shipping address."
    )
    phone = models.CharField(
        max_length=20, blank=True, help_text="Contact phone number."
    )
    reference_id = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="External reference ID for the address.",
    )
    email = models.EmailField(blank=True, null=True, help_text="Contact email address.")

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    def __str__(self) -> str:
        return f"{self.buyer_name} - {self.city}, {self.country}"
