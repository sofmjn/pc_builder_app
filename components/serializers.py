# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Build
from .models import (
    Component, CPU, GPU, RAM, Motherboard, PSU, Case,
    Build
)

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = ['socket', 'tdp', 'chipset_support']


class MotherboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motherboard
        fields = ['socket', 'chipset', 'ram_type', 'max_ram_freq', 'form_factor']


class RAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = RAM
        fields = ['ram_type', 'frequency', 'capacity_gb']


class GPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPU
        fields = ['length_mm', 'tdp', 'pcie_version']


class PSUSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSU
        fields = ['wattage', 'efficiency']


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['max_gpu_length', 'motherboard_support']

class ComponentSerializer(serializers.ModelSerializer):
    specific = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = ['id', 'name', 'type', 'price', 'vendor', 'specific']

    def get_specific(self, obj):
        if hasattr(obj, obj.type):
            model_instance = getattr(obj, obj.type, None)
            serializer_class = {
                'cpu': CPUSerializer,
                'gpu': GPUSerializer,
                'ram': RAMSerializer,
                'motherboard': MotherboardSerializer,
                'psu': PSUSerializer,
                'case': CaseSerializer,
            }.get(obj.type)
            if serializer_class and model_instance:
                return serializer_class(model_instance).data
        return None

class BuildSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    components = ComponentSerializer(many=True, read_only=True)
    component_ids = serializers.PrimaryKeyRelatedField(
        queryset=Component.objects.all(),
        many=True,
        write_only=True,
        source='components',
        required=False
    )

    total_price = serializers.SerializerMethodField()
    components_by_type = serializers.SerializerMethodField()

    class Meta:
        model = Build
        fields = [
            'id', 'user', 'name', 'description',
            'components', 'component_ids',
            'created_at', 'updated_at',
            'total_price', 'components_by_type'
        ]
    def get_components_by_type(self, obj):
        grouped = {}
        for component in obj.components.all():
            grouped.setdefault(component.type, []).append({
                "id": component.id,
                "name": component.name,
                "price": component.price,
                "vendor": component.vendor,
            })
        return grouped

    def get_total_price(self, obj):
        return obj.total_price()

    def validate_name(self, value):
        user = self.context['request'].user
        if self.instance and self.instance.name == value:
            return value
        if Build.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError("Build with this name already exists")
        return value

    def update(self, instance, validated_data):
        components = validated_data.pop('components', None)
        if components is not None:
            for component in components:
                instance.components.add(component)
        return super().update(instance, validated_data)