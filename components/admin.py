from django.contrib import admin
from .models import Component, Build

@admin.register(Component)

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'brand', 'price')
    search_fields = ('name', 'brand', 'type')
    list_filter = ('type', 'brand')

@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')
    filter_horizontal = ('components',)  

# Register your models here.
