from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from corner_test.apps.access.views import (
    LoginView,
    RefreshTokenView,
    VerifyTokenView,
)
from corner_test.apps.menus.views import (
    OrderListViewSet,
    MenuCreateUpdateDeleteViewSet,
    DishListUpdateCreateDeleteViewSet,
    MenuListAPIView,
)
from corner_test.apps.utils.views import (
    DailyMenuReminderNotificationAPIView,
    OrderSlackReadAPIView,
)


menu_router = DefaultRouter()
menu_router.register(r"orders", OrderListViewSet)
menu_router.register(r"menu", MenuCreateUpdateDeleteViewSet)
menu_router.register(r"dishes", DishListUpdateCreateDeleteViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "send_menu_reminder/",
        DailyMenuReminderNotificationAPIView.as_view(),
        name="send_reminder",
    ),
    path("get_orders/", OrderSlackReadAPIView.as_view(), name="get_orders"),
    path("api/v1/", include(menu_router.urls)),
    path("api/v1/menus/", MenuListAPIView.as_view()),
    path("api/v1/users/login/", LoginView.as_view(), name="login"),
    path("api/v1/users/refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("api/token/verify/", VerifyTokenView.as_view(), name="token_verify"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/doc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
