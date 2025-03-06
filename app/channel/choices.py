from django.db.models import TextChoices


class ChannelState(TextChoices):
    # Create your models here.
    ACTIVE = "ACTIVE", "Active"
    DEACTIVE = "DEACTIVE", "Deactive"
    FAILED = "FAILED", "Failed"
    PROCESSING = "PROCESSING", "Processing"
    OTHER = "OTHER", "Other"
