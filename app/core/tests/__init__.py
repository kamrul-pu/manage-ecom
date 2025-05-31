import factory
from factory.django import DjangoModelFactory
from faker import Faker

from core.models import User, Organization
from core.choices import UserKind, UserGender

fake = Faker()


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker("company")
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(" ", "-"))
    description = factory.Faker("sentence")
    email = factory.Faker("company_email")
    location = factory.Faker("city")
    subscription = factory.Faker("boolean")
    expiration_date = factory.Faker("future_datetime")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    organization = factory.SubFactory(OrganizationFactory)
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone = factory.Faker("phone_number")
    gender = factory.Iterator(UserGender.values)
    kind = factory.Iterator(UserKind.values)
    is_active = True
    is_staff = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted if extracted else "testpassword123"
        self.set_password(password)
        if create:
            self.save()
