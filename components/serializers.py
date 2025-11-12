# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Component, Build

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'

class BuildSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    components = ComponentSerializer(many=True, read_only=True)
    component_ids = serializers.PrimaryKeyRelatedField(
        queryset=Component.objects.all(), many=True, write_only=True, source='components', required=False
    )

    total_price = serializers.SerializerMethodField()
    components_by_type = serializers.SerializerMethodField()

    class Meta:
        model = Build
        fields = ['id', 'user', 'name', 'description', 'components', 'component_ids', 'created_at', 'updated_at', 'total_price', 'components_by_type']
    
    def get_components_by_type(self, obj):
        grouped = {}
        for component in obj.components.all():
            grouped.setdefault(component.type, []).append({
                "id": component.id,
                "name": component.name,
                "price": component.price,
                "link": component.link
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
        # если пришли новые компоненты Ч обновл€ем
        components = validated_data.pop('components', None)
        if components is not None:
            for component in components:
                instance.components.add(component)
        # остальные пол€ (например name)
        return super().update(instance, validated_data)