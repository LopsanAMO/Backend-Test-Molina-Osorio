from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

@extend_schema(
    description="Login",
    operation_id="Login",
    tags=["Access"]
)
class LoginView(TokenObtainPairView):
    pass


@extend_schema(
    description="Refresh Token Access",
    operation_id="Refresh_Token",
    tags=["Access"]
)
class RefreshTokenView(TokenRefreshView):
    pass


@extend_schema(
    description="Verify Token Access",
    operation_id="Token_Verify",
    tags=["Access"]
)
class VerifyTokenView(TokenVerifyView):
    pass