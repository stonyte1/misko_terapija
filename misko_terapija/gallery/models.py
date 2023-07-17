from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Gallery(models.Model):
    photo = models.ImageField(_("photo"), upload_to='gallery/', blank=True, null=True)

    class Meta:
        verbose_name = _("gallery")
        verbose_name_plural = _("gallerys")

    def __str__(self):
        return f'{self.photo}'

    def get_absolute_url(self):
        return reverse("gallery_detail", kwargs={"pk": self.pk})
