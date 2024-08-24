from django.shortcuts import render
from rest_framework import viewsets
from .models import Category,Product
from .serializers import CategorySerializer,ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser) 
    def create(self, request, *args, **kwargs):
        # Handle file upload if necessary
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Handle file upload if necessary
        return super().update(request, *args, **kwargs)