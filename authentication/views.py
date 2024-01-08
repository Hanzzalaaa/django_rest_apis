from rest_framework import generics, permissions
from .serializers import *
# from .utils import *
from rest_framework.response import Response
from rest_framework import status
# Create your views here.  
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
# from django_rest_passwordreset.urls


class UserRegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer




class UserLoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer





