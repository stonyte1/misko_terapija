# Generated by Django 4.2.3 on 2023-07-07 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_alter_client_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='surname',
        ),
    ]