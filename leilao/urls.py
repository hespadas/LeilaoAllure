from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_screen, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("product/<int:bidid>", views.product, name="product"),
    path("bid", views.bid, name="bid"),
    path("winnings", views.winnings, name="winnings"),
    path("winner", views.winner, name="winner"),
]
