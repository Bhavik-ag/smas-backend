from rest_framework import serializers
from .models import CustomUser

class UserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'password', 'roll_no', 'is_staff', 'is_active')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}