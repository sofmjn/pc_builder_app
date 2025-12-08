from rest_framework import generics, filters, permissions
from .models import Component, Build
from .serializers import ComponentSerializer, BuildSerializer
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ComponentFilter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .services import CompatibilityChecker
import random
from rest_framework.generics import ListAPIView




class ComponentListView(generics.ListAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ComponentFilter

    search_fields = ['name', 'vendor', 'type']
    ordering_fields = ['price', 'name']

class ComponentDetailView(generics.RetrieveAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [AllowAny]

class CheckCompatibilityView(APIView):

    def post(self, request):
        comp_ids = request.data.get("components", [])

        comps = Component.objects.filter(id__in=comp_ids)
        typed = {c.type: getattr(c, c.type) for c in comps if hasattr(c, c.type)}

        checker = CompatibilityChecker()
        result = checker.check_build(
            cpu=typed.get("cpu"),
            gpu=typed.get("gpu"),
            ram=typed.get("ram"),
            mobo=typed.get("motherboard"),
            psu=typed.get("psu"),
            case=typed.get("case")
        )

        return Response({"compatibility": result})

class BuildListCreateView(generics.ListCreateAPIView):
    serializer_class = BuildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Берем все сборки текущего пользователя
        queryset = Build.objects.filter(user=self.request.user)
        
        # Получаем параметр ?name= из запроса
        name_query = self.request.query_params.get('name')
        if name_query:
            # Фильтруем по частичному совпадению в имени сборки, регистр не важен
            queryset = queryset.filter(name__icontains=name_query)
        
        return queryset


    def perform_create(self, serializer):
        # Автоматически присваиваем текущего пользователя
        serializer.save(user=self.request.user)


class BuildDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BuildSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Пользователь может видеть и менять только свои сборки
        return Build.objects.filter(user=self.request.user)

class BuildCompatibilityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        build = get_object_or_404(Build, pk=pk, user=request.user)

        components_dict = {}
        for c in build.components.all():
            if hasattr(c, c.type):
                specific = {}
                related_obj = getattr(c, c.type)
              
                for field in related_obj._meta.get_fields():
                    if field.name != "component" and hasattr(related_obj, field.name):
                        specific[field.name] = getattr(related_obj, field.name)
                
                components_dict[c.type] = {
                    "id": c.id,
                    "name": c.name,
                    "type": c.type,
                    "price": str(c.price) if c.price else None,
                    "vendor": c.vendor,
                    "specific": specific
                }

        checker = CompatibilityChecker()
        result = checker.check_build(
            cpu=components_dict.get("cpu"),
            gpu=components_dict.get("gpu"),
            ram=components_dict.get("ram"),
            mobo=components_dict.get("motherboard"),
            psu=components_dict.get("psu"),
            case=components_dict.get("case")
        )

        formatted = [{"ok": r[0], "message": r[1]} for r in result]

        return Response({
            "build_id": build.id,
            "compatibility": formatted
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_component_from_build(request, pk):
    
    build = get_object_or_404(Build, pk=pk, user=request.user)

    component_ids = request.data.get('component_ids')
    if not component_ids:
        return Response({"detail": "component_ids is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Фильтруем компоненты, которые реально есть в сборке
    components = build.components.filter(id__in=component_ids)
    if not components.exists():
        return Response({"detail": "No matching components in this build"}, status=status.HTTP_400_BAD_REQUEST)

    for component in components:
        build.components.remove(component)

    build.save()
    serializer = BuildSerializer(build)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_component_to_build(request, pk):
    
    build = get_object_or_404(Build, pk=pk, user=request.user)
    
    # Получаем component_ids из запроса
    component_ids = request.data.get('component_ids')
    if not component_ids:
        return Response({"detail": "component_ids is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Проверяем что все компоненты существуют
    components = Component.objects.filter(id__in=component_ids)
    if not components.exists():
        return Response({"detail": "No valid components found"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Добавляем компоненты
    for component in components:
        build.components.add(component)
    
    build.save()
    
    serializer = BuildSerializer(build)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Create your views here.
