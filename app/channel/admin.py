from django.contrib import admin

# Register your models here.
from .models import Channel


class ChannelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uid",
        "name",
        "channel_type",
        "channel_state",
    )


admin.site.register(Channel, ChannelAdmin)
