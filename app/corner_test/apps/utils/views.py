from rest_framework import permissions
from rest_framework.response import Response
from corner_test.apps.menus.tasks import send_today_menu, save_messages
from corner_test.apps.menus.serializers import FakeSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import generics


@extend_schema(description="Mandar notificacion de menu a slack")
class DailyMenuReminderNotificationAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = FakeSerializer

    def post(self, request):
        send_today_menu()
        return Response(status=200)


@extend_schema(description="Leer pedidos de slack")
class OrderSlackReadAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = FakeSerializer

    def post(self, request):
        save_messages()
        return Response(status=200)
