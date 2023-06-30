from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class Reservation(models.Model):
    date_from = models.DateField(_("from"), default=None)
    date_to = models.DateField(_("to"), default=None)
    

    class Meta:
        verbose_name = _("reservation")
        verbose_name_plural = _("reservations")

    def __str__(self):
        return f'{self.date_from} - {self.date_to}'

    def get_absolute_url(self):
        return reverse("reservation_detail", kwargs={"pk": self.pk})

class Client(models.Model):
    name = models.CharField(_("name"), max_length=250)
    surname = models.CharField(_("surname"), max_length=250)
    email = models.CharField(_("email"), max_length=250)
    phone_number = PhoneNumberField()
    reservation = models.ForeignKey(
        Reservation, 
        verbose_name=_("reservation"), 
        on_delete=models.CASCADE,
        related_name='clients'
        )
    
    class Meta:
        verbose_name = _("client")
        verbose_name_plural = _("clients")

    def __str__(self):
        return f'{self.name}: {self.email}'

    def get_absolute_url(self):
        return reverse("client_detail", kwargs={"pk": self.pk})
