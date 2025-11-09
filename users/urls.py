from django.urls import path
from .views import RegisterView,UserDetailView, LoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),   # Регистрация
    path('login/', LoginAPIView.as_view(), name='login'),  # Логин
    path('me/', UserDetailView.as_view(), name='user-detail'), #эндпоинт текущего пользователя
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
]
