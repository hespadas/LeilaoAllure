from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    pass


class Products(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    name = models.CharField("Produto:", max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, null=True)
    starting_bid = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Bids(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    product = models.IntegerField()
    highest_bid = models.IntegerField()


class Winner(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    bid_win_list = models.ForeignKey(Products, on_delete=models.CASCADE)
