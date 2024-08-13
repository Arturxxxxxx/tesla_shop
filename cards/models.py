import datetime
from django.db import models

class Category(models.Model):
    image = models.ImageField(upload_to='category/',blank=True, null=True)
    category = models.CharField(max_length=50, unique=True, verbose_name="Категория")

    def __str__(self) -> str:
        return self.category

class Product(models.Model):
    CHOICE_NEW = 'Новый'
    CHOICE_USED = 'Б/У'
    
    CHOICE_OPTIONS = [
        (CHOICE_NEW, 'Новый'),
        (CHOICE_USED, 'БУ'),
    ]
    image1 = models.ImageField(upload_to="cards/")
    image2 = models.ImageField(upload_to="cards/")
    image3 = models.ImageField(upload_to="cards/")
    image4 = models.ImageField(upload_to="cards/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=300)
    artikul = models.PositiveIntegerField()
    year = models.PositiveIntegerField() 
    in_stock = models.BooleanField(default=True)
    model = models.CharField(max_length=50)
    spare_part_number = models.CharField(max_length=50)
    generation = models.CharField(max_length=50)
    choice = models.CharField(
        max_length=6,
        choices=CHOICE_OPTIONS,
        default=CHOICE_NEW,
    )
    created_at = models.DateTimeField(default=datetime.datetime.now) 

    def __str__(self):
        return self.title