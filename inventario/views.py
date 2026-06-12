from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Producto
from .serializers import ProductoSerializer
from .scraping import scrapear_productos

class ProductoListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

class ActualizarProductosView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        productos = scrapear_productos()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)