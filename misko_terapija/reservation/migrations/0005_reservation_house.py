# Generated by Django 4.2.2 on 2023-07-03 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        ('reservation', '0004_remove_reservation_email_remove_reservation_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='house',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='home.house', verbose_name='houses'),
        ),
    ]