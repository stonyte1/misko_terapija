from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Image(models.Model):
    photo = models.ImageField(_("photo"), upload_to='house/', blank=True, null=True)
    

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")

    def __str__(self):
        return f'{self.photo}'

    def get_absolute_url(self):
        return reverse("image_detail", kwargs={"pk": self.pk})


class House(models.Model):
    name = models.CharField(_("name"), max_length=250)
    main_image = models.ImageField(_("main_image"), upload_to='house/', blank=True, null=True)
    price = models.FloatField(_("price"), null=True, blank=True)
    guests = models.IntegerField(_("guests"))
    beds = models.CharField(_("beds"), max_length=50)
    content = models.TextField(_("content"), blank=True, null=True)
    images = models.ManyToManyField(
        Image,
        verbose_name=_("images"),
        related_name='houses',
        related_query_name='house',
        blank=True
    )

    class Meta:
        verbose_name = _("house")
        verbose_name_plural = _("houses")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("house_detail", kwargs={"pk": self.pk})

