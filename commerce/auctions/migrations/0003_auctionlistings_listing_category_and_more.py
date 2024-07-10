# Generated by Django 5.0.6 on 2024-07-10 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlistings'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='listing_category',
            field=models.CharField(choices=[('VEH', 'Vehicles'), ('FAS', 'Fashion'), ('DEV', 'Devices'), ('TOO', 'Tools'), ('SPO', 'Sports'), ('TOY', 'Toys'), ('ENT', 'Entertainment'), ('MIS', 'Miscellanious')], default='MIS', max_length=3),
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='listing_photo',
            field=models.URLField(blank=True),
        ),
    ]
