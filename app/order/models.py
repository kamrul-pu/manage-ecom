from django.db import models
from common.models import BaseModelWithUID


class Order(BaseModelWithUID):
    channel = models.ForeignKey(
        "channel.Channel",
        related_name="channel_orders",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="The sales channel this order originates from.",
    )
    channel_order_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique order ID from the channel.",
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("PAID", "Paid"),
            ("FAILED", "Failed"),
            ("REFUNDED", "Refunded"),
        ],
        default="PENDING",
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
        max_length=3, default="USD", help_text="Currency code (e.g., USD, EUR)."
    )
    total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, help_text="Total order amount."
    )
    company_uid = models.CharField(
        max_length=36, db_index=True, help_text="Unique identifier for the company."
    )
    market_place = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Marketplace name (e.g., Amazon, eBay).",
    )
    dispatch_status = models.CharField(
        max_length=20,
        choices=[
            ("OPEN_ORDER", "Open Order"),
            ("CLOSED", "Closed"),
            ("DISPATCHED", "Dispatched"),
            ("FAILED", "Failed"),
            ("CANCELLED", "Cancelled"),
            ("PENDING", "Pending"),
        ],
        default="OPEN_ORDER",
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
        indexes = [
            models.Index(fields=["channel_order_id", "company_uid"]),
        ]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def get_order_items_sku_list(self):
        """Return a list of remote SKUs for order items."""
        return list(self.order_items.values_list("remote_sku", flat=True))

    def get_order_item_sku_quantity(self):
        """Return a list of dictionaries with SKU, quantity, and UIDs."""
        return list(
            self.order_items.values(
                "remote_sku", "quantity", "channel_uid", "company_uid"
            )
        )


class OrderItem(BaseModelWithUID):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
        help_text="The order this item belongs to.",
    )
    remote_sku = models.CharField(
        max_length=128, blank=True, null=True, help_text="SKU from the remote channel."
    )
    local_sku = models.CharField(
        max_length=128, blank=True, null=True, help_text="Local SKU if mapped."
    )
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
    # channel_uid = models.CharField(
    #     max_length=36, help_text="Unique identifier for the channel."
    # )
    # company_uid = models.CharField(
    #     max_length=36, help_text="Unique identifier for the company."
    # )
    position_item_ids = models.JSONField(
        blank=True,
        null=True,
        default=list,
        help_text="List of position item IDs (replaced ArrayField for portability).",
    )
    picked_sku = models.CharField(
        max_length=128, blank=True, null=True, help_text="SKU of the picked item."
    )
    picked_at = models.DateTimeField(
        blank=True, null=True, help_text="Date and time the item was picked."
    )
    picked_item_type = models.CharField(
        max_length=20,
        choices=[
            ("EXACT_ITEM", "Exact Item"),
            ("EXCHANGE_ITEM", "Exchange Item"),
        ],
        blank=True,
        null=True,
        help_text="Type of picked item.",
    )
    packed_sku = models.CharField(
        max_length=128, blank=True, null=True, help_text="SKU of the packed item."
    )
    packed_at = models.DateTimeField(
        blank=True, null=True, help_text="Date and time the item was packed."
    )

    class Meta:
        indexes = [
            models.Index(fields=["remote_sku", "local_sku"]),
            # models.Index(fields=["channel_uid", "company_uid"]),
        ]
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def save(self, *args, **kwargs):
        """Automatically calculate total_amount if not provided."""
        if self.price is not None and self.quantity is not None:
            self.total_amount = self.price * self.quantity
        super().save(*args, **kwargs)


class OrderShippingAddress(BaseModelWithUID):
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
        verbose_name = "Order Shipping Address"
        verbose_name_plural = "Order Shipping Addresses"
