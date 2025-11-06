from rest_framework import generics, filters, permissions
from .models import Component, Build
from .serializers import ComponentSerializer, BuildSerializer
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ComponentFilter


class ComponentListView(generics.ListAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ComponentFilter

    search_fields = ['name', 'brand', 'type']
    ordering_fields = ['price', 'name']

class ComponentDetailView(generics.RetrieveAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [AllowAny]

class BuildListCreateView(generics.ListCreateAPIView):
    serializer_class = BuildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Показываем только сборки текущего пользователя
        return Build.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Автоматически присваиваем текущего пользователя
        serializer.save(user=self.request.user)


class BuildDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BuildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Пользователь может видеть и менять только свои сборки
        return Build.objects.filter(user=self.request.user)

# Create your views here.
