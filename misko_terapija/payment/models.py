from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from reservation.models import Client


class UserPayment(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
        )
    #Makes sure if payment went througt customer 
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

#Created payment recordevery time new user is created
@receiver(post_save, sender=Client)
def create_client_payment(sender, instance, created, **kwargs):
    if created: 
        UserPayment.objects.create(client=instance)