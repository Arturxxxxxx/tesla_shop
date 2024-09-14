from django.db import models
from django.utils import timezone

class Category(models.Model):
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    category = models.CharField(max_length=50, unique=True, verbose_name="Категория")

    def __str__(self) -> str:
        return self.category

class Product(models.Model):
    CHOICE_NEW = 'Новый'
    CHOICE_USED = 'Б/У'
    
    CHOICE_OPTIONS = [
        (CHOICE_NEW, 'Новый'),
        (CHOICE_USED, 'Б/У'),
    ]
    title = models.CharField(max_length=250)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=300)
    artikul = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    spare_part_number = models.CharField(max_length=50)
    generation = models.CharField(max_length=50)
    choice = models.CharField(
        max_length=6,
        choices=CHOICE_OPTIONS,
        default=CHOICE_NEW,
    )
    created_at = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # images = models.JSONField(default=list, blank=True, null=True)
    image = models.ImageField(upload_to='posts_img', blank=True, verbose_name='Фото')


    def __str__(self):
        return self.title


