from django.contrib import admin

from leilao.models import Products, Bids, User


# Register your models here.
@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "slug", "user", "active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Bids)
class BidsAdmin(admin.ModelAdmin):
    list_display = ("product", "highest_bid", "user")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "date_joined")
