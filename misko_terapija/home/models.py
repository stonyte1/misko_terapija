from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Image(models.Model):

    

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("image_detail", kwargs={"pk": self.pk})


class House(models.Model):
    name = models.CharField(_("name"), max_length=250)
    main_image = models.ImageField(_("main_image"), upload_to='house/', blank=True, null=True)
    image = models.ImageField(_("image"), upload_to='house/', blank=True, null=True)
    guests = models.IntegerField(_("guests"))
    beds = models.CharField(_("beds"), max_length=50)
    content = models.TextField(_("content"), blank=True, null=True)

    class Meta:
        verbose_name = _("house")
        verbose_name_plural = _("houses")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("house_detail", kwargs={"pk": self.pk})

