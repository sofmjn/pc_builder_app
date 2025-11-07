from django.db import models
from django.contrib.auth.models import User

class Component(models.Model):
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

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=COMPONENT_TYPES)
    brand = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    compatibility = models.TextField(blank=True)  # позже можно заменить на связи между моделями
    link = models.URLField(blank=True)  # ссылка на DNS или другой магазин

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Build(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='builds')
    name = models.CharField(max_length=100)
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
