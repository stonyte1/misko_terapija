# Generated by Django 4.2.3 on 2023-07-07 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_alter_client_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='reservation.reservation', verbose_name='reservation'),
        ),
    ]