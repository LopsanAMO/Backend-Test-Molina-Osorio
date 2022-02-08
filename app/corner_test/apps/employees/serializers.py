from rest_framework import serializers
from corner_test.apps.employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("name",)
