from django.db.models import TextChoices


class DispatchStatus(TextChoices):
    CLOSED = "CLOSED", "Closed"
    CANCELLED = "CANCELLED", "Cancelled"
    DISPATCHED = "DISPATCHED", "Dispatched"
    FAILED = "FAILED", "Failed"
    OPEN_ORDER = "OPEN_ORDER", "Open Order"
    PENDING = "PENDING", "Pending"
    RETURNED = "RETURNED", "Returned"


class PickedItemType(TextChoices):
    EXACT_ITEM = "EXACT_ITEM", "Exact_Item"
    EXCHANGE_ITEM = "EXCHANGE_ITEM", "Exchange_Item"


class PaymentStatus(TextChoices):
    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"
    FAILED = "FAILED", "Failed"
    REFUNDED = "REFUNDED", "Refunded"
