# Generated by Django 5.0.6 on 2024-07-11 16:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auctionlistings_listing_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='listing_category',
            field=models.CharField(choices=[('VEH', 'Vehicles'), ('FAS', 'Fashion'), ('DEV', 'Devices'), ('TOO', 'Tools'), ('SPO', 'Sports'), ('TOY', 'Toys'), ('ENT', 'Entertainment'), ('MIS', 'Miscellanious')], max_length=3),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=400)),
                ('comment_auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_on', to='auctions.auctionlistings')),
                ('comment_maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_made', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
