from django.db import models

from pojazd.models import Pojazd



class Zapytanie(models.Model):

    zapytanie_id = models.CharField(max_length=50)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    regon = models.CharField(max_length=50)
    urodzenie_data = models.DateField(null=True)
    pojazd = models.ForeignKey(Pojazd, null=True, on_delete=models.SET_NULL)
    rozpoczecie_polisy_data = models.DateField()

