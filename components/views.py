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
from .pagination import ComponentPagination
from .services import CompatibilityChecker
import random
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q




class ComponentListView(generics.ListAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [AllowAny]
    pagination_class = ComponentPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ComponentFilter

    search_fields = ['name', 'vendor', 'type']
    ordering_fields = ['price', 'name']

class ComponentDetailView(generics.RetrieveAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [AllowAny]

class CheckCompatibilityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        comp_ids = request.data.get("components", []) or []
        comps = (Component.objects
                 .filter(id__in=comp_ids)
                 .select_related("cpu", "gpu", "ram", "motherboard", "psu", "case"))

        serialized = ComponentSerializer(comps, many=True).data
        typed = {}
        for item in serialized:
            typed[item["type"]] = item  # если 2 одинаковых типа — последний перезапишет

        checker = CompatibilityChecker()
        result = checker.check_build(
            cpu=typed.get("cpu"),
            gpu=typed.get("gpu"),
            ram=typed.get("ram"),
            mobo=typed.get("motherboard"),
            psu=typed.get("psu"),
            case=typed.get("case"),
        )

        formatted = [{"ok": ok, "message": msg} for (ok, msg) in result]
        return Response({"compatibility": formatted})

class CandidatesPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100

class ComponentCandidatesView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ComponentSerializer
    pagination_class = CandidatesPagination

    def post(self, request):
        target_type = request.data.get("target_type")
        selected_ids = request.data.get("selected_component_ids", []) or []
        compatibility = bool(request.data.get("compatibility", True))

        search = (request.data.get("search") or "").strip()
        vendors = request.data.get("vendor")  # строка или список
        price_min = request.data.get("price_min")
        price_max = request.data.get("price_max")

        if not target_type:
            return Response({"detail": "target_type is required"}, status=400)

        qs = (Component.objects
              .filter(type=target_type)
              .select_related("cpu", "gpu", "ram", "motherboard", "psu", "case"))

        # ---- обычные фильтры ----
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(vendor__icontains=search))

        if vendors:
            if isinstance(vendors, str):
                vendors = [vendors]
            qs = qs.filter(vendor__in=vendors)

        if price_min not in (None, ""):
            qs = qs.filter(price__gte=price_min)
        if price_max not in (None, ""):
            qs = qs.filter(price__lte=price_max)

        # ---- фильтр совместимости ----
        if compatibility and selected_ids:
            selected = (Component.objects
                        .filter(id__in=selected_ids)
                        .select_related("cpu", "gpu", "ram", "motherboard", "psu", "case"))

            cpu = next((c.cpu for c in selected if c.type == "cpu" and hasattr(c, "cpu")), None)
            gpu = next((c.gpu for c in selected if c.type == "gpu" and hasattr(c, "gpu")), None)
            ram = next((c.ram for c in selected if c.type == "ram" and hasattr(c, "ram")), None)
            mobo = next((c.motherboard for c in selected if c.type == "motherboard" and hasattr(c, "motherboard")), None)
            psu = next((c.psu for c in selected if c.type == "psu" and hasattr(c, "psu")), None)
            case = next((c.case for c in selected if c.type == "case" and hasattr(c, "case")), None)

            # MOTHERBOARD под CPU
            if target_type == "motherboard" and cpu:
                qs = qs.filter(
                    motherboard__socket=cpu.socket,
                    motherboard__chipset__in=cpu.chipset_support,
                )

            # CPU под MOTHERBOARD
            elif target_type == "cpu" and mobo:
                qs = qs.filter(
                    cpu__socket=mobo.socket,
                    cpu__chipset_support__contains=[mobo.chipset],  # JSONField list contains
                )

            # RAM под MOTHERBOARD
            elif target_type == "ram" and mobo:
                qs = qs.filter(
                    ram__ram_type=mobo.ram_type,
                    ram__frequency__lte=mobo.max_ram_freq,
                )

            # CASE под GPU
            elif target_type == "case" and gpu:
                qs = qs.filter(case__max_gpu_length__gte=gpu.length_mm)

            # PSU под CPU+GPU
            elif target_type == "psu" and cpu and gpu:
                required = int((cpu.tdp + gpu.tdp) * 1.4)
                qs = qs.filter(psu__wattage__gte=required)

            # (опционально) GPU под CASE — если хочешь в обе стороны
            elif target_type == "gpu" and case:
                qs = qs.filter(gpu__length_mm__lte=case.max_gpu_length)

        page = self.paginate_queryset(qs.order_by("id"))
        ser = self.get_serializer(page, many=True)
        return self.get_paginated_response(ser.data)

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
