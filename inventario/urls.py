from django.urls import path
from .views import ProductoListView, ActualizarProductosView

urlpatterns = [
    path('productos/', ProductoListView.as_view()),
    path('productos/actualizar/', ActualizarProductosView.as_view()),
]