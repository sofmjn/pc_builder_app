from django.db import models
from django.contrib.auth.models import User


COMPONENT_TYPES = [
        ('cpu', 'Processor'),
        ('gpu', 'Graphics Card'),
        ('motherboard', 'Motherboard'),
        ('ram', 'Memory (RAM)'),
        ('storage', 'Storage (SSD/HDD)'),
        ('psu', 'Power Supply'),
        ('case', 'Case'),
        ('cooler', 'Cooling System'),
    ]
class Component(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    vendor = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

class CPU(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="cpu")
    socket = models.CharField(max_length=50)
    tdp = models.IntegerField()  # тепловыделение в Вт
    chipset_support = models.JSONField(default=list) 

class Motherboard(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="motherboard")
    socket = models.CharField(max_length=50)
    chipset = models.CharField(max_length=50)
    ram_type = models.CharField(max_length=20)  # DDR4/DDR5
    max_ram_freq = models.IntegerField()
    form_factor = models.CharField(max_length=20)  # ATX/mATX/ITX

class RAM(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="ram")
    ram_type = models.CharField(max_length=20)  # DDR4/DDR5
    frequency = models.IntegerField()
    capacity_gb = models.IntegerField()

class GPU(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="gpu")
    length_mm = models.IntegerField()
    tdp = models.IntegerField()
    pcie_version = models.CharField(max_length=10, default="4.0")

class PSU(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="psu")
    wattage = models.IntegerField()
    efficiency = models.CharField(max_length=10, null=True, blank=True)

class Case(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE, related_name="case")
    max_gpu_length = models.IntegerField()
    motherboard_support = models.JSONField(default=list)


# === BUILD ===

class Build(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='builds')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)  
    components = models.ManyToManyField(Component, related_name='builds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_build_name_per_user')
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    def total_price(self):
        return sum(c.price or 0 for c in self.components.all())

# Create your models here.
