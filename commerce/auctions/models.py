from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    VEHICLES = "VEH"
    FASHINON = "FAS"
    DEVICES = "DEV"
    TOOLS = "TOO"
    SPORTS = "SPO"
    TOYS = "TOY"
    ENTERTAINMENT = "ENT"
    MISCELLANIOUS = "MIS"

    CATEGORY = [
        (VEHICLES, "Vehicles"),
        (FASHINON, "Fashion"),
        (DEVICES, "Devices"),
        (TOOLS, "Tools"),
        (SPORTS, "Sports"),
        (TOYS, "Toys"),
        (ENTERTAINMENT, "Entertainment"),
        (MISCELLANIOUS, "Miscellanious")
    ]
    
    listing_name = models.CharField(max_length=64)
    listing_description = models.CharField(max_length=128)
    listing_photo = models.URLField(blank=True, max_length=4000)
    listing_starting = models.IntegerField()
    listing_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings_made')
    listing_category = models.CharField(max_length=3, choices=CATEGORY)
    listing_status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.listing_name}'

class Comment(models.Model):
    comment_text = models.CharField(max_length=400)
    comment_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_made')
    comment_auction = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name='comments_on')

    def __str__(self):
        return f'{self.comment_auction} commented on by {self.comment_maker}'

class Watchlist(models.Model):
    watchlist_listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name='in_watchlists')
    watchlist_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist_items')

    def __str__(self):
        return f'{self.watchlist_listing} in watchlist of {self.watchlist_maker}'

class Bid(models.Model):
    bid_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids_made')
    bid_item = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.IntegerField()

    def __str__(self):
        return f'{self.bid_maker} bid {self.bid_amount} on {self.bid_item}'

    def clean(self):
        if self.bid_amount < self.bid_item.listing_starting:
            raise ValidationError(f'Bid amount cannot be less than the starting price of {self.bid_item.listing_starting}.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)