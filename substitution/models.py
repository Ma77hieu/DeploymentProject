from django.db import models
# if __name__ == "main":
#     from authentification.models import User
# else:
#     from ..authentification.models import User
from authentification.models import User
# from django.contrib.auth.models import User


# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=500)
    nutrition_grade = models.CharField(max_length=1)
    url = models.CharField(max_length=255)
    image_front_small_url = models.CharField(max_length=255)
    energy_kj = models.CharField(max_length=45)
    energy_kcal = models.CharField(max_length=45)
    fat = models.CharField(max_length=45)
    fiber = models.CharField(max_length=45)
    proteins = models.CharField(max_length=45)
    salt = models.CharField(max_length=45)
    average_rating = models.CharField(max_length=45,null=True, blank=True,default=None)

    def __str__(self):
        return self.product_name


class Categories(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class Favorites(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product

# class Ratings(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     class Rating (models.IntegerChoices):
#         ZERO=0
#         UN=1
#         DEUX=2
#         TROIS=3
#         QUATRE=4
#         CINQ=5
#     rating = models.IntegerField(choices=Rating.choices)

class Ratings(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return self.product
