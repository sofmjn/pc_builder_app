from django.urls import path
from .views import ComponentListView, ComponentDetailView, BuildListCreateView, BuildDetailView

urlpatterns = [
    path('', ComponentListView.as_view(), name='component-list'),
    path('<int:pk>/', ComponentDetailView.as_view(), name='component-detail'),
    path('builds/', BuildListCreateView.as_view(), name='build-list'),
    path('builds/<int:pk>/', BuildDetailView.as_view(), name='build-detail'),
]
