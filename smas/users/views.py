import datetime
from django.conf import settings

from .models import CustomUser
from .serializers import UserSerialzer
from .authentication import CustomJWTAuthentication

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            
            access_token = response.data["access"]
            refresh_token = response.data["refresh"]
            
            user = CustomUser.objects.get(email=request.data['email'])
            serializer = UserSerialzer(user, many=False)
            response.data['user'] = serializer.data
            
            response.set_cookie(
                "access",
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )

            response.set_cookie(
                "refresh",
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )
            
        return response
    
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data["access"]

            response.set_cookie(
                "access",
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )

        return response


class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerialzer
    permission_classes = [IsAdminUser]
    
class GenerateQRHash(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        user = CustomUser.objects.get(email=request.user)
        print(user.roll_no)
        hash = str(user.id) + str(user.roll_no) + str(datetime.datetime.now())
        return Response({'hash': hash})