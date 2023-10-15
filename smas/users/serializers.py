from rest_framework import serializers
from .models import CustomUser, Meal

class UserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'password', 'roll_no', 'is_staff', 'is_active')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
        
class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'meal_date', 'has_breakfast', 'has_lunch', 'has_dinner', 'breakfast_time', 'lunch_time', 'dinner_time')
        extra_kwargs = {'student': {'read_only': True}}