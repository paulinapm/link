from django.db import models


class Pojazd(models.Model):

    marka = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    rocznik = models.PositiveIntegerField(null=True)
