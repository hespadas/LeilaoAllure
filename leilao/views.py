from django.shortcuts import render, redirect
from leilao.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError


# Create your views here.


def index(request):
    return render(
        request,
        "index.html",
        {
            "active_list": Products.objects.filter(active=True),
        },
    )


def login_screen(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        return render(
            request, "login.html", {"message": "Username ou password inválidos"}
        )
    return render(
        request, "login.html", {"message": "Username ou password inválidos"}
    )


@login_required(login_url="login")
def create(request):
    if request.method == "POST":
        p = Products()
        try:
            p.user = request.user
        except TypeError:
            p.user = User(user=request.user)
        p.name = request.POST["create_name"]
        p.description = request.POST["create_desc"]
        p.starting_bid = request.POST["create_initial_bid"]
        p.save()
        return redirect("index")
    return render(request, "create.html")


# this function returns minimum bid required to place a user's bid@login_required(login_url="login")
def bid(request: object) -> object:
    """
    this function returns minimum bid required to place a user's bid@login_required(login_url="login")
    :param request:
    :return: object
    """
    valor_bid = request.GET["valor_bid"]
    list_id = request.GET["product_id"]
    bid_present = Bids.objects.filter(product=list_id)
    starting_bid = Products.objects.get(pk=list_id)
    min_bid = starting_bid.starting_bid
    for bid in bid_present:
        if min_bid < int(bid.highest_bid):
            min_bid = int(bid.highest_bid)
    if int(valor_bid) > int(min_bid):
        newbid = Bids(user=request.user, product=list_id, highest_bid=valor_bid)
        newbid.save()
    messages.warning(
        request, f"Sorry, {valor_bid} is less. It should be more than {min_bid}$."
    )
    return product(request, list_id)


def minbid(min_bid, present_bid):

    return min_bid


def product(request, bidid):
    item = Products.objects.get(pk=bidid, active=True)
    bid_present = Bids.objects.filter(product=bidid)
    min_bid = item.starting_bid
    for bid in bid_present:
        if min_bid < int(bid.highest_bid):
            min_bid = int(bid.highest_bid)
    return render(
        request,
        "product.html",
        {"product": item, "present_bid": min_bid},
    )


def winner(request):
    bid_id = request.GET["itemid"]
    bid_present = Bids.objects.filter(product=bid_id)
    biddesc = Products.objects.get(pk=bid_id, active=True)
    max_bid = minbid(biddesc.starting_bid, bid_present)
    try:
        winner_object = Bids.objects.get(highest_bid=max_bid, product=bid_id)
        winner_obj = Products.objects.get(id=bid_id)
        win = Winner(bid_win_list=winner_obj, user=winner_object.user)
        winners_name = winner_object.user
    except:
        winner_obj = Products.objects.get(starting_bid=max_bid, id=bid_id)
        win = Winner(bid_win_list=winner_obj, user=winner_obj.user)
        winners_name = winner_obj.user


    biddesc.active = False
    biddesc.save()

    # saving winner details
    win.save()
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "register.html", {"message": "Passwords estão diferentes"}
            )
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "register.html", {"message": "Este usuário já existe"}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


# checks winner
def winnings(request):
    vencedor = Winner.objects.filter(user=request.user)
    return render(
        request,
        "winnings.html",
        {
            "user_winlist": vencedor,
        },
    )


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
