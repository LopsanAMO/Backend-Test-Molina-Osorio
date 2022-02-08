import factory
from corner_test.apps.employees.tests.factories import EmployeeFactory
from corner_test.apps.menus.models import Menu, Order, Dish


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    date = factory.Faker("date")


class DishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dish

    name = factory.Sequence(lambda n: f"name_{n}")
    description = factory.Sequence(lambda n: f"description_{n}")
    menu = factory.SubFactory(MenuFactory)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    dish = factory.SubFactory(DishFactory)
    specifications = factory.Sequence(lambda n: f"specifications_{n}")
    employee = factory.SubFactory(EmployeeFactory)
    created_at = factory.Faker("date")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"testuser{n}")
    password = factory.Faker(
        "password",
        length=10,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = True
