from django.db import models
from django.contrib.auth import get_user_model

from common.models import NameSlugDescriptionBaseModel
from .choices import AuthType, StoreStatus
from common.choices import MarketPlace


# User = get_user_model()


class Store(NameSlugDescriptionBaseModel):
    # user = models.ForeignKey(
    #     User,
    #     related_name="channels",
    #     on_delete=models.CASCADE,
    # )
    organization = models.ForeignKey(
        "core.Organization",
        related_name="stores",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    auth_type = models.CharField(
        max_length=20, choices=AuthType.choices, default=AuthType.BASIC, blank=True
    )
    store_type = models.CharField(max_length=20)
    store_status = models.CharField(
        max_length=30, choices=StoreStatus.choices, default=StoreStatus.OTHER
    )
    marketplace = models.CharField(
        max_length=128,
        choices=MarketPlace.choices,
        default=MarketPlace.OTHER,
        blank=True,
    )
    shop_url = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=128, blank=True)
    max_stock = models.PositiveIntegerField(default=0, blank=True)
    report_ref = models.JSONField(blank=True, default=dict)
    report_sorted_by = models.CharField(max_length=128, blank=True)
    is_authorized = models.BooleanField(default=True)
    expires_on = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    access_token = models.CharField(max_length=512, blank=True)
    refresh_token = models.CharField(max_length=512, blank=True)
    access_token_expiry = models.BigIntegerField(default=0, blank=True, null=True)
    refresh_token_expiry = models.BigIntegerField(default=0, blank=True, null=True)
    metadata = models.JSONField(blank=True, default=dict)
    order_sync = models.BooleanField(default=False, blank=True)
    inventory_sync = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Stores"

    def __str__(self):
        return f"{self.name} {self.marketplace} {self.country} {self.store_type}"


from django.db import models
from common.models import NameSlugDescriptionBaseModel


class Warehouse(NameSlugDescriptionBaseModel):
    """
    Represents a physical or virtual location where goods are stored for a store.
    """

    store = models.ForeignKey(
        "store.Store",
        related_name="warehouses",
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        max_length=50, unique=True, help_text="Unique warehouse identifier"
    )
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    is_primary = models.BooleanField(
        default=False, help_text="Set if this is the store's main warehouse"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Warehouses"
        unique_together = ("store", "code")

    def __str__(self):
        return f"{self.name} - {self.code} ({self.city}, {self.country})"
