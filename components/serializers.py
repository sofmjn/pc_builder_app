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

    class Meta:
        model = Build
        fields = ['id', 'user', 'name', 'components', 'component_ids', 'created_at', 'updated_at']

    def validate_name(self, value):
        user = self.context['request'].user
        if Build.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError("Build with this name already exists")
        return value