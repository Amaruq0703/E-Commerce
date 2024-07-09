# Generated by Django 5.0.6 on 2024-07-09 15:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionListings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_name', models.CharField(max_length=64)),
                ('listing_description', models.CharField(max_length=128)),
                ('listing_photo', models.ImageField(blank=True, default='listingimages/Image_not_available.png', upload_to='listingimages')),
                ('listing_starting', models.IntegerField()),
                ('listing_maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings_made', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
