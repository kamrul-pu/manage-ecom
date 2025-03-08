from django.db import models
from django.contrib.auth import get_user_model

from common.models import NameSlugDescriptionBaseModel
from .choices import ChannelState


User = get_user_model()


class Channel(NameSlugDescriptionBaseModel):
    user = models.ForeignKey(
        User,
        related_name="channels",
        on_delete=models.CASCADE,
    )
    channel_type = models.CharField(max_length=20)
    channel_state = models.CharField(
        max_length=30, choices=ChannelState.choices, default=ChannelState.OTHER
    )
    market_place = models.CharField(max_length=128, blank=True)
    shop_url = models.CharField(max_length=256, blank=True)
    country = models.CharField(max_length=128, blank=True)
    channel_max_stock = models.PositiveIntegerField(default=0, blank=True)
    report_ref = models.JSONField(blank=True, default=dict)
    report_sorted_by = models.CharField(max_length=128, blank=True)
    is_authorized = models.BooleanField(default=True)
    expires_on = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    channel_metadata = models.JSONField(blank=True, default=dict)
    order_sync = models.BooleanField(default=False, blank=True)
    inventory_sync = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Channels"

    def __str__(self):
        return f"{self.name} {self.market_place} {self.country} {self.channel_type}"
