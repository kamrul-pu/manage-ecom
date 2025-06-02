from django.db.models import TextChoices


class Action(TextChoices):
    ADDITION = "ADDITION", "Addition"
    SUBTRACTION = "SUBTRACTION", "Subtraction"
    FULL_STOCK = "FULL_STOCK", "Full_Stock"
    NEW_ORDER_ITEM = "NEW_ORDER_ITEM", "New_Order_Item"
    CANCEL_ORDER_ITEM = "CANCEL_ORDER_ITEM", "Cancel_Order_Item"
    DISPATCH_ORDER_ITEM = "DISPATCH_ORDER_ITEM", "Dispatch_Order_Item"
    RETURN = "RETURN", "Return"


class RequestStatus(TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    PROCESSING = "PROCESSING", "Processing"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"
