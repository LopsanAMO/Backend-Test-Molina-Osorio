from django.db import IntegrityError
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    OpenApiResponse,
)
from datetime import datetime
from rest_framework import mixins, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from corner_test.apps.menus.models import Order, Menu, Dish
from corner_test.apps.menus.serializers import (
    OrderSerializer,
    MenuCreateUpdateSerializer,
    DishSerializer,
    MenuListSerializer,
)
from corner_test.apps.utils.slack import SlackService
from django.conf import settings


class OrderListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.filter(created_at=datetime.now().date())

    @extend_schema(
        description="Get the orders from slack",
        operation_id="Orders.List",
        tags=["Order"],
    )
    def list(self, request, *args, **kwargs):
        service = SlackService(settings.SLACK_API_KEY)
        service.get_messages()
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MenuCreateUpdateDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MenuCreateUpdateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Menu.objects.all()

    @extend_schema(
        description="Crete a menu",
        operation_id="Menu.Create",
        tags=["Menu"],
    )
    def create(self, request, *args, **kwargs):
        return super(MenuCreateUpdateDeleteViewSet, self).create(
            request, *args, **kwargs
        )

    @extend_schema(
        description="Get Menu information",
        operation_id="Menu.Retrieve",
    )
    def create(self, request, *args, **kwargs):
        return super(MenuCreateUpdateDeleteViewSet, self).retrieve(
            request, *args, **kwargs
        )

    @extend_schema(
        description="Update Menus",
        operation_id="Menu.Update",
        tags=["Menu"],
    )
    def update(self, request, *args, **kwargs):
        return super(MenuCreateUpdateDeleteViewSet, self).update(
            request, *args, **kwargs
        )

    @extend_schema(
        description="Delete Menus",
        operation_id="Menu.Delete",
        tags=["Menu"],
    )
    def destroy(self, request, *args, **kwargs):
        return super(MenuCreateUpdateDeleteViewSet, self).destroy(
            request, *args, **kwargs
        )


class MenuListAPIView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        description="List all todays menu",
        operation_id="Menus.List",
        tags=["Menu"],
        responses={
            200: OpenApiResponse(response=MenuListSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = Menu.objects.get(date=datetime.today())
            serializer = MenuListSerializer(queryset)
            return Response(data=serializer.data)
        except Menu.DoesNotExist:
            return Response(data={"message": "no menu found for today"}, status=200)


class DishListUpdateCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = DishSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Dish.objects.all()

    @extend_schema(
        description="List all Dishes",
        operation_id="Dish.List",
        tags=["Dish"],
    )
    def list(self, request, *args, **kwargs):
        return super(DishListUpdateCreateDeleteViewSet, self).list(
            request, *args, **kwargs
        )

    @extend_schema(
        description="Create a Dish for menu",
        operation_id="Dish.Create",
        tags=["Dish"],
    )
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except IntegrityError as e:
            return Response(
                data={"error": "integrity_error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                data={"error": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        description="Update a Dish",
        operation_id="Dish.Update",
        tags=["Dish"],
    )
    def update(self, request, *args, **kwargs):
        return super(DishListUpdateCreateDeleteViewSet, self).update(
            request, *args, **kwargs
        )

    @extend_schema(
        description="Delete a Dish",
        operation_id="Dish.Delete",
        tags=["Dish"],
    )
    def destroy(self, request, *args, **kwargs):
        return super(DishListUpdateCreateDeleteViewSet, self).destroy(
            request, *args, **kwargs
        )
