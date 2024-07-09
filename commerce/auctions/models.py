from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListings(models.Model):
    listing_name = models.CharField(max_length=64)
    listing_description = models.CharField(max_length=128)
    listing_photo = models.ImageField(upload_to='listingimages', blank=True, default='listingimages/Image_not_available.png')
    listing_starting = models.IntegerField()
    listing_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings_made')

