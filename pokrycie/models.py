from django.db import models

from zakres.models import Zakres


class Pokrycie(models.Model):

    nazwa = models.CharField(max_length=50)
    ubezpieczenie_suma = models.PositiveIntegerField()
    zakres = models.ForeignKey(Zakres, null=True, on_delete=models.SET_NULL)

