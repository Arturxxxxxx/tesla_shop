from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
