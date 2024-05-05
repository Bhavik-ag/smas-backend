from django.urls import path
from .views import UserList, GenerateQRHash, CustomTokenObtainPairView, CustomTokenRefreshView, VerifyQRHash, MealList, MealStats, MealStatsForStudent, AddUser, RetrieveUser, MealStatsForAll


urlpatterns = [
    path('', UserList.as_view(), name='user-list'),
    path('generate/', GenerateQRHash.as_view(), name='generate'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', VerifyQRHash.as_view(), name='verify'),    
    path('meals/', MealList.as_view(), name='meal-list'),
    path('meals-stats/', MealStats.as_view(), name='meal-stats'),
    path('admin/mealsstats/', MealStatsForStudent.as_view(), name='meal-stats-for-student'),
    path('admin/mealsstatsforall/', MealStatsForAll.as_view(), name='meal-stats-for-all'),
    path('add/', AddUser.as_view(), name='add-user'),
    path('retrieve/', RetrieveUser.as_view(), name='retrieve-user'),
]
