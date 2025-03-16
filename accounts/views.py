from accounts.models import CustomUser
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import RegisterSerializer, CustomUserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils import custom_response
from constants import (
    SUCCESS_USER_REGISTERED,
    SUCCESS_LOGOUT,
    ERROR_INVALID_REFRESH_TOKEN,
    ERROR_SOMETHING_WENT_WRONG, ERROR_USER_REGISTRATION_FAILED, ERROR_FETCHING_PROFILE
)


# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return custom_response(SUCCESS_USER_REGISTERED, response.data, status.HTTP_201_CREATED)
        except Exception as e:
            return custom_response(ERROR_USER_REGISTRATION_FAILED, [], status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user
        except Exception as e:
            return custom_response(ERROR_FETCHING_PROFILE, str(e), status.HTTP_400_BAD_REQUEST)

# User Logout View
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Logout user by blacklisting refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist')
            },
            required=['refresh']
        ),
        responses={205: "Token successfully blacklisted", 400: "Invalid refresh token"}
    )
    def post(self, request):
        refresh_token = request.data.get("refresh", None)
        if not refresh_token:
            return custom_response(ERROR_INVALID_REFRESH_TOKEN, [], status_code=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return custom_response(SUCCESS_LOGOUT, [], status_code=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return custom_response(ERROR_SOMETHING_WENT_WRONG, [], status_code=status.HTTP_400_BAD_REQUEST)
