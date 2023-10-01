from django.urls import path
from .views import UserList, GenerateQRHash
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', UserList.as_view(), name='user-list'),
    path('generate/', GenerateQRHash.as_view({'get': 'list'}), name='generate'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
