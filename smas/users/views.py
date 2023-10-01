import datetime
from .models import CustomUser
from rest_framework import generics, viewsets
from .serializers import UserSerialzer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerialzer
    permission_classes = [IsAdminUser]
    
class GenerateQRHash(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        user = CustomUser.objects.get(email=request.user)
        print(user.roll_no)
        hash = str(user.id) + str(user.roll_no) + str(datetime.datetime.now())
        return Response({'hash': hash})