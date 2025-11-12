from django.urls import path
from .views import ComponentListView, ComponentDetailView, BuildListCreateView, BuildDetailView, add_component_to_build, remove_component_from_build

urlpatterns = [
    path('', ComponentListView.as_view(), name='component-list'),
    path('<int:pk>/', ComponentDetailView.as_view(), name='component-detail'),
    path('builds/', BuildListCreateView.as_view(), name='build-list'),
    path('builds/<int:pk>/', BuildDetailView.as_view(), name='build-detail'),
    path('builds/<int:pk>/add_component/', add_component_to_build, name='add-component-to-build'),
    path('builds/<int:pk>/remove_component/', remove_component_from_build, name='remove-component-from-build'),

]
