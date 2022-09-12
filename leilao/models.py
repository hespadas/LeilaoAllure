from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass


class Products(models.Model):
    user = models.CharField(max_length=64)
    product_name = models.CharField("Produto:", max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, null=True)
    starting_bid = models.IntegerField()

    def __str__(self):
        return self.product_name


class Bids(models.Model):
    user = models.CharField(max_length=30)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    highest_bid = models.IntegerField()