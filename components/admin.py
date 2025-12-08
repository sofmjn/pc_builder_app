from django.contrib import admin
from .models import Component, Build
from .models import CPU, Motherboard, RAM, GPU, PSU, Case

admin.site.register(CPU)
admin.site.register(Motherboard)
admin.site.register(RAM)
admin.site.register(GPU)
admin.site.register(PSU)
admin.site.register(Case)


@admin.register(Component)

class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'vendor', 'price')
    search_fields = ('name', 'vendor', 'type')
    list_filter = ('type', 'vendor')

@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')
    filter_horizontal = ('components',)  

# Register your models here.
