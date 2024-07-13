from django.contrib import admin
from auctions.models import *
# Register your models here.

admin.site.register(AuctionListings)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bid)