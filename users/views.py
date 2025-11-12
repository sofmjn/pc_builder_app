from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Доступно для всех, даже неавторизованных
    serializer_class = RegisterSerializer

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # доступ только авторизованным

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })
# Create your views here.

class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # чтобы не требовать токен

    def post(self, request):
        identifier = request.data.get('identifier')  # email или username
        password = request.data.get('password')
        
        if not identifier or not password:
            return Response({"detail": "Enter email or username"}, status=400)

        # Ищем пользователя
        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                return Response({"detail": "Incorect personal details"}, status=401)

        # Проверка пароля
        if not user.check_password(password):
            return Response({"detail": "Icorect personal details"}, status=401)

        # Генерируем токены
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
            
        })