from django.contrib import admin
from auctions.models import *
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_name", "listing_starting", "listing_category", "listing_maker", "listing_status")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment_maker", "comment_auction", "comment_text")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "watchlist_listing", "watchlist_maker")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bid_maker", "bid_item", "bid_amount")

admin.site.register(AuctionListings, ListingAdmin)
admin.site.register(User)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid, BidAdmin)