# Generated by Django 4.2.3 on 2023-08-19 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_review_remove_house_image_house_price_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='price_weekend',
            field=models.FloatField(blank=True, null=True, verbose_name='price_weekend'),
        ),
    ]
