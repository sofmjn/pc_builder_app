from django.urls import path
from .views import RegisterView,UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),   # Регистрация
    path('login/', TokenObtainPairView.as_view(), name='login'),  # Логин
    path('me/', UserDetailView.as_view(), name='user-detail'), #эндпоинт текущего пользователя
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
]
