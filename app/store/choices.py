from django.db.models import TextChoices


class AuthType(TextChoices):
    BASIC = "BASIC", "Basic"
    OAUTH = "OAUTH", "OAuth"
    OAUTH2 = "OAUTH2", "OAuth2"
    TOKEN = "TOKEN", "Token"


class MarketPlace(TextChoices):
    AMAZON = "AMAZON", "Amazon"
    BIG_COMMERCE = "BIG_COMMERCE", "BigCommerce"
    EBAY = "EBAY", "eBay"
    OTTO = "OTTO", "Otto"
    SHEIN = "SHEIN", "Shein"
    SHOPIFY = "SHOPIFY", "Shopify"
    TEMU = "TEMU", "Temu"
    TIKTOK_SHOP = "TIKTOK_SHOP", "TikTok Shop"
    WOOCOMMERCE = "WOOCOMMERCE", "WooCommerce"
    OTHER = "OTHER", "Other"


class StoreStatus(TextChoices):
    # Create your models here.
    ACTIVE = "ACTIVE", "Active"
    DEACTIVE = "DEACTIVE", "Deactive"
    FAILED = "FAILED", "Failed"
    PROCESSING = "PROCESSING", "Processing"
    OTHER = "OTHER", "Other"
