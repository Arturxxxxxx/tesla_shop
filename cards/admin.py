from django.contrib import admin
from .models import Category, Product, Marka
from django.utils.safestring import mark_safe

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Marka)


