from django.db import models
from pokrycie.models import Pokrycie


class Odpowiedz(models.Model):

    skladka = models.DecimalField(max_digits=6, decimal_places=2)
    pokrycie_list = models.ManyToManyField(Pokrycie)
    czy_klient_szkodowy = models.BooleanField()

