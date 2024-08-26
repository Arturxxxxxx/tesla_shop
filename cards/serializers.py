from rest_framework import serializers
from .models import Category, Product
   
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    image_urls = serializers.SerializerMethodField()

    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'description', 'artikul', 'year', 'in_stock',
            'model', 'marka', 'spare_part_number', 'generation', 'choice', 'created_at',
            'category', 'category_name', 'images', 'image_urls'
        ]

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)

        image_paths = []
        for image in images:
            path = f'products/{image.name}'
            image_paths.append(path)
            with open(f'media/{path}', 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)

        product.images = image_paths
        product.save()

        return product

    def get_category_name(self, obj):
        return obj.category.category


    def get_image_urls(self, obj):
        request = self.context.get('request')
        return [request.build_absolute_uri(f'/media/{image}') for image in obj.images]