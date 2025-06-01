from django.db.models import TextChoices


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


class Status(TextChoices):
    ACTIVE = "ACTIVE", "Active"
    DRAFT = "DRAFT", "DRAFT"
    INACTIVE = "INACTIVE", "Inactive"
    REMOVED = "REMOVED", "Removed"
    VERIFIED = "VERIFIED", "Verified"
