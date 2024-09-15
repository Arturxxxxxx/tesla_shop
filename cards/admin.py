from django.contrib import admin
from .models import Category, Product
from django.utils.safestring import mark_safe

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)

