from django.contrib import admin
from corner_test.apps.menus.models import Menu, Dish, Order


admin.site.register(Menu)
admin.site.register(Dish)
admin.site.register(Order)
