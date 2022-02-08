from django.db import transaction
from django.db import IntegrityError
from rest_framework import serializers
from corner_test.apps.menus.models import Menu, Dish, Order
from corner_test.apps.employees.serializers import EmployeeSerializer
from corner_test.apps.menus.exceptions import MenuDateException


class MenuSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ("options", "id")

    def get_options(self, obj):
        return [
            "Option {}: {}".format(option.id, option.name)
            for option in obj.dish_set.all()
        ]


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ("name", "description", "id", "menu")

    def to_representation(self, instance):
        ret = super(DishSerializer, self).to_representation(instance)
        for key, value in ret.items():
            if key == "menu":
                ret[key] = str(value)
        return ret

    def validate_menu(self, value):
        if value in [None, ""]:
            raise serializers.ValidationError("menu dont be null or empty")
        return value


class SimpleDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ("name", "description", "id")


class MenuCreateUpdateSerializer(serializers.ModelSerializer):
    options = SimpleDishSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = ("options",)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                options = validated_data.pop("options", None)
                try:
                    menu = Menu.objects.create(**validated_data)
                except IntegrityError as e:
                    raise MenuDateException(
                        "menu's today already exists, please edit or delete it"
                    )
                for i in options:
                    Dish.objects.create(menu=menu, **i)
                return menu
        except MenuDateException as e:
            raise serializers.ValidationError(detail={"error": str(e)})
        except Exception as e:
            raise serializers.ValidationError(detail={"error": str(e)})


class MenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("date", "dish_set", "id")
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    employee = EmployeeSerializer()

    class Meta:
        model = Order
        fields = ("dish", "specifications", "employee")


class FakeSerializer(serializers.Serializer):
    fake_field = serializers.CharField(required=False)
