from django.db import models


class Zakres(models.Model):

    amortyzacja = models.BooleanField()
    dostepnosc_warunkowa = models.BooleanField()
