import uuid
from datetime import datetime
from django.db import models
from corner_test.apps.employees.models import Employee


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(unique=True, default=datetime.today())


class Dish(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, blank=True)


class Order(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT)
    specifications = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    created_at =  models.DateField(auto_now_add=True)