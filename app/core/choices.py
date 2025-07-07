from django.db.models import TextChoices


class UserKind(TextChoices):
    ADMIN = "ADMIN", "Admin"
    CLIENT = "CLIENT", "Client"
    DEVELOPER = "DEVELOPER", "Developer"
    MANAGER = "MANAGER", "Manager"
    EMPLOYEE = "EMPLOYEE", "Employee"
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    UNDEFINED = "UNDEFINED", "Undefined"


class UserGender(TextChoices):
    FEMALE = "FEMALE", "Female"
    MALE = "MALE", "Male"
    UNKNOWN = "UNKNOWN", "Unknown"
    OTHER = "OTHER", "Other"
