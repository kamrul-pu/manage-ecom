from django.contrib import admin

from product.models import LocalProduct, RemoteProduct

# Register your models here.


class LocalProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uid",
        "name",
        "slug",
        "sku",
    )


admin.site.register(LocalProduct, LocalProductAdmin)


class RemoteProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uid",
        "name",
        "slug",
        "sku",
    )


admin.site.register(RemoteProduct, RemoteProductAdmin)
