from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html
# Register your models here.


admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('images', 'title', 'category', 'price', 'artikul', 'year', 'in_stock', 'choice', 'marka', 'created_at')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />'.format(obj.image.url))
        return "No Image"

    image_tag.short_description = 'Image'

admin.site.register(Product, ProductAdmin)
    
