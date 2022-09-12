from django.contrib import admin

from leilao.models import Products, Bids, User


# Register your models here.
@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", "description", "slug")
    prepopulated_fields = {"slug": ("product_name",)}


@admin.register(Bids)
class BidsAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "highest_bid")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "date_joined")
