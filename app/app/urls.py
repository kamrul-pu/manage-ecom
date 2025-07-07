"""
Main URL Mapping of the app.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import permissions


urlpatterns = [
    path("admin/", admin.site.urls),
    # include user endpoints
    path("api/v1/users", include("core.urls.user"), name="user-urls"),
    # include organization endpoints
    path(
        "api/v1/organizations",
        include("core.urls.organization"),
        name="organization-urls",
    ),
    # include store urls
    path("api/v1/stores", include("store.urls.store"), name="store-related-urls"),
    # include warehouse urls
    path("api/v1/warehouses", include("store.urls.warehouse"), name="warehouse-urls"),
    # include product urls
    path("api/v1/products", include("product.urls.base"), name="product-urls"),
    # include order urls
    path("api/v1/orders", include("order.urls.base"), name="order-urls"),
    # include inventory urls
    path(
        "api/v1/inventory", include("inventory.urls.base"), name="inventory-base-urls"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # drf yasg api documentation
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="E-COM Manager Backend API",
            version="1.0.0",
            default_version="1.0",
            description="Test description",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns += [
        path(
            "swagger<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "api/docs",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]

if settings.ENABLE_SILK:
    urlpatterns += [re_path(r"^profiler/", include("silk.urls", namespace="silk"))]
