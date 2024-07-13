from django.contrib import admin
from auctions.models import *
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing_name", "listing_starting", "listing_category", "listing_maker", "listing_status")

admin.site.register(AuctionListings, ListingAdmin)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bid)