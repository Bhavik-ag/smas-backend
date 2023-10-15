import datetime
from django.conf import settings

from .models import CustomUser, Meal
from .serializers import UserSerialzer, MealSerializer

from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

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
    
class GenerateQRHash(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        student = CustomUser.objects.get(email=request.user)
        today = datetime.datetime.today().astimezone(tz=datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
        meal_instance, created = Meal.objects.get_or_create(student=student, meal_date=today)
        
        breakfast_start_time = today.replace(hour=7)
        lunch_start_time = today.replace(hour=12)   
        dinner_start_time = today.replace(hour=18)
        meal_duration = datetime.timedelta(hours=3)
        
        breakfast_end_time = breakfast_start_time + meal_duration
        lunch_end_time = lunch_start_time + meal_duration
        dinner_end_time = dinner_start_time + meal_duration

        current_time = datetime.datetime.now(tz=datetime.timezone.utc).astimezone(tz=datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
        
        response_data = {}
        meal_type = 'breakfast'
        
        if breakfast_start_time <= current_time < breakfast_end_time:
            meal_type = 'breakfast'
            if meal_instance.has_breakfast:
                response_data['message'] = 'You have already had a meal today.'
        elif lunch_start_time <= current_time < lunch_end_time:
            meal_type = 'lunch'
            if meal_instance.has_lunch:
                response_data['message'] = 'You have already had a meal today.'
        elif dinner_start_time <= current_time < dinner_end_time:
            meal_type = 'dinner'
            if meal_instance.has_dinner:
                response_data['message'] = 'You have already had a meal today.'
                
        response_data['meal'] = meal_type
        
        # Generate a user and meal specific hash here
        response_data['hash'] = student.email + meal_type + str(today)
            
        return Response(response_data)
                     
class VerifyQRHash(views.APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        email, meal_type = self.decrypt(request.data['hash'])
        student = CustomUser.objects.get(email=email)
        
        if not student:
            return Response({'message': 'This student does not exist.'}, status=HTTP_400_BAD_REQUEST)
        
        today = datetime.datetime.today().astimezone(tz=datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
        
        if not student.is_active:
            return Response({'message': 'This student has been deactivated.'}, status=HTTP_400_BAD_REQUEST)
        
        meal_instance, created = Meal.objects.get_or_create(student=student, meal_date=today)
        
        if meal_type == 'breakfast':
            if meal_instance.has_breakfast:
                return Response({'message': 'This student has already had breakfast.'}, status=HTTP_400_BAD_REQUEST)
            meal_instance.has_breakfast = True
            meal_instance.breakfast_time = datetime.datetime.now()
            
        elif meal_type == 'lunch':
            if meal_instance.has_lunch:
                return Response({'message': 'This student has already had lunch.'}, status=HTTP_400_BAD_REQUEST)
            meal_instance.has_lunch = True
            meal_instance.lunch_time = datetime.datetime.now()
            
        elif meal_type == 'dinner':
            if meal_instance.has_dinner:
                return Response({'message': 'This student has already had dinner.'}, status=HTTP_400_BAD_REQUEST)
            meal_instance.has_dinner = True
            meal_instance.dinner_time = datetime.datetime.now()
            
        meal_instance.save()
        
        return Response({'message': 'Meal verified successfully.'}, status=HTTP_200_OK)
        
    def decrypt(self, hash):
        email = hash.split('@')[0] + '@iiitdmj.ac.in'
        
        if "breakfast" in hash:
            meal_type = "breakfast"
        elif "lunch" in hash:
            meal_type = "lunch"
        elif "dinner" in hash:
            meal_type = "dinner"
            
        return email, meal_type
        
class MealList(generics.ListAPIView):
    serializer_class = UserSerialzer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        student = CustomUser.objects.get(email=self.request.user)
        return Meal.objects.filter(student=student)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MealSerializer(queryset, many=True)
        return Response(serializer.data)