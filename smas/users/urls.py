from django.urls import path
from .views import UserList, GenerateQRHash, CustomTokenObtainPairView, CustomTokenRefreshView, VerifyQRHash, MealList

urlpatterns = [
    path('', UserList.as_view(), name='user-list'),
    path('generate/', GenerateQRHash.as_view(), name='generate'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', VerifyQRHash.as_view(), name='verify'),    
    path('meals/', MealList.as_view(), name='meal-list'),
]
