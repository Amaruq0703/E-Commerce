from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *


class NewListingForm(forms.Form):
    listing_name = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder' : 'Enter Product Name',
            'required' : 'True', 
            'class': 'form-control'
        }), label='Listing Name', required=False)
    
    listing_description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter Product Description',
        'required' : 'True',
        'class': 'form-control'
    }), label="Description", required=False)

    listing_starting = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Starting Price',
        'required' : 'True',
        'class': 'form-control'
    }), label="Starting Price", required=False)

    listing_photo = forms.URLField(widget=forms.URLInput(attrs={
        'placeholder': 'Enter Image URL',
        'required' : 'True',
        'class': 'form-control'
    }), label="Photo", required=False)

    listing_category = forms.ChoiceField(choices=AuctionListings.CATEGORY, widget=forms.Select(attrs={
        'placeholder': 'Choose Category',
        'required' : 'True',
        'class': 'form-control'
    }), label="", required=False)



def index(request):        
    return render(request, "auctions/index.html", {
        'listings' : AuctionListings.objects.all(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def make_listing(request, username):
    listingform = NewListingForm(request.POST, request.FILES)
    
    if request.method == 'POST':
        listing_name = request.POST.get('listing_name')
        listing_description = request.POST.get('listing_description')
        listing_starting = request.POST.get('listing_starting')
        listing_photo = request.POST.get('listing_photo')
        listing_maker = User.objects.get(pk=request.user.id)

        auction_listing = AuctionListings(listing_name=listing_name, listing_description=listing_description, listing_starting=listing_starting, listing_photo=listing_photo, listing_maker=listing_maker)
        auction_listing.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/makelisting.html', {
            'listingform' : listingform,
        })