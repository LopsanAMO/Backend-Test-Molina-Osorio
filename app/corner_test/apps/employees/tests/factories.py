import factory
from corner_test.apps.employees.models import Employee


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    slack_user_id = factory.Sequence(lambda n: f"slack_user_id_{n}")
    channel_id = factory.Sequence(lambda n: f"channel_id_{n}")
    name = factory.Sequence(lambda n: f"name_{n}")
