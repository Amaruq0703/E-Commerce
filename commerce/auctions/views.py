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

class CommentForm(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder' : 'Comment on this Listing...',
        'required' : 'True',
        'class' : 'form-control'
    }), label="")

class BidForm(forms.Form):
    bid_amount = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder' : 'Bid on this Listing...',
        'required' : 'True',
        'class' : 'form-control'
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
    
def make_listing(request):
    listingform = NewListingForm(request.POST, request.FILES)
    
    if request.method == 'POST':
        listing_name = request.POST.get('listing_name')
        listing_description = request.POST.get('listing_description')
        listing_starting = request.POST.get('listing_starting')
        listing_photo = request.POST.get('listing_photo')
        listing_maker = User.objects.get(pk=request.user.id)
        listing_category = request.POST.get('listing_category')

        auction_listing = AuctionListings(listing_name=listing_name, listing_description=listing_description, listing_starting=listing_starting, listing_photo=listing_photo, listing_maker=listing_maker, listing_category=listing_category, listing_status = True)
        auction_listing.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'auctions/makelisting.html', {
            'listingform' : listingform,
        })
    
def viewlisting(request, auction_id):
    listing = AuctionListings.objects.get(pk = auction_id)
    comments = Comment.objects.filter(comment_auction = listing)
    commentform = CommentForm()
    watchlist_items = Watchlist.objects.filter(watchlist_listing = listing)
    watchlist_user = User.objects.get(pk=request.user.id)
    watchlist_bool = Watchlist.objects.filter(watchlist_listing = listing, watchlist_maker = watchlist_user)
    bids = listing.bids.all()
    winner_bid = bids.order_by('-bid_amount').first()

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        comment_auction = listing
        comment_maker = User.objects.get(pk=request.user.id)

        comment = Comment(comment_text=comment_text, comment_auction=comment_auction, comment_maker=comment_maker)
        comment.save()
        return HttpResponseRedirect(reverse('viewlisting', kwargs={'auction_id' : listing.id,}))
    
    return render(request, 'auctions/listingpage.html', {
        'listing' : listing,
        'comments' : comments,
        'commentform' : commentform,
        'watchlist_items' : watchlist_items,
        'watchlist_bool' : watchlist_bool,
        'bids' : bids,
        'user' : watchlist_user,
        'winner_bid' : winner_bid
    })

def watchlist(request, auction_id):
    listing = AuctionListings.objects.get(pk = auction_id)
    watchlist_user = User.objects.get(pk=request.user.id)
    watchlist_bool = Watchlist.objects.filter(watchlist_listing = listing, watchlist_maker = watchlist_user)
    if watchlist_bool:
        watchlist_bool.delete()
    else:
        w = Watchlist(watchlist_listing = listing, watchlist_maker = watchlist_user)
        w.save()

    return HttpResponseRedirect(reverse('viewlisting', kwargs={'auction_id' : listing.id, }))
        

def watchlist_page(request, username):
    user = User.objects.get(pk=request.user.id)
    watchlist_items = user.watchlist_items.all()
    return render(request, 'auctions/watchlist_page.html', {
        'watchlist_items' : watchlist_items
    })

def bid(request, auction_id):
    item = AuctionListings.objects.get(pk=auction_id)
    bidform = BidForm(request.POST)
    if request.method == 'POST':  
        if bidform.is_valid():
            bid_amount = bidform.cleaned_data['bid_amount']
            user = User.objects.get(pk=request.user.id) 
            bid = Bid(bid_maker = user, bid_item = item, bid_amount=bid_amount)
            try:
                bid.save()
                return HttpResponseRedirect(reverse('viewlisting', kwargs={'auction_id' : auction_id, }))
            except ValidationError as e:
                bidform.add_error('bid_amount', e.message)
            
    
    return render(request, 'auctions/bidpage.html', {
        'bidform' : bidform,
        'auction_id': auction_id,
        'item' : item
    })
    
def closelisting(request, auction_id):

    listing = AuctionListings.objects.get(pk=auction_id)
    bids = listing.bids.all()
    winner_bid = bids.order_by('-bid_amount').first()
    winner = winner_bid.bid_maker.username
    listing.listing_status=False
    listing.save()

    return render(request, 'auctions/closelisting.html', {
        'winner' : winner
    })

def viewcategories(request):

    categories = AuctionListings.CATEGORY

    return render(request, 'auctions/categories.html', {
        'categories' : categories
    })

def category(request, category_name):
    listings = AuctionListings.objects.filter(listing_category = category_name)

    return render(request, 'auctions/categorypage.html', {
        'listings' : listings,
        'category_name' : category_name
    })

