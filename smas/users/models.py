from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin   
from django.utils import timezone

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=10, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    data_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager() 
    
    def __str__(self):
        return self.email   
    
class Meal(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    meal_date = models.DateField()
    has_breakfast = models.BooleanField(default=False)
    has_lunch = models.BooleanField(default=False)
    has_dinner = models.BooleanField(default=False)
    
    # Store timestamp of when the meal was taken
    breakfast_time = models.DateTimeField(blank=True, null=True)
    lunch_time = models.DateTimeField(blank=True, null=True)
    dinner_time = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('student', 'meal_date')