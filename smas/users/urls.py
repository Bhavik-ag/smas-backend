from django.urls import path
from .views import UserList, GenerateQRHash, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('', UserList.as_view(), name='user-list'),
    path('generate/', GenerateQRHash.as_view({'get': 'list'}), name='generate'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
