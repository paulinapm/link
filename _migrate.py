import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "link.settings")

import django
django.setup()

import json

from django.db import transaction

from odpowiedz.models import Odpowiedz
from pojazd.models import Pojazd
from pokrycie.models import Pokrycie
from zakres.models import Zakres
from zapytanie.models import Zapytanie

Odpowiedz.objects.all().delete()
Pojazd.objects.all().delete()
Pokrycie.objects.all().delete()
Zakres.objects.all().delete()
Zapytanie.objects.all().delete()


with transaction.atomic():
    # Opening JSON file
    f = open('zadanie_rekrutacyjne_przyklady.json')

    # returns JSON object as a dictionary
    data = json.load(f)
    
    try:
        for zapytanie in data['zapytanie']:
            z = Zapytanie.objects.create(
                    zapytanie_id=zapytanie['idzapytania'],
                    imie=zapytanie['imie'],
                    nazwisko=zapytanie['nazwisko'],
                    regon='' if zapytanie['regon'] is None else zapytanie['regon'],
                    urodzenie_data=zapytanie['dataurodzenia'],
                    rozpoczecie_polisy_data=zapytanie['datarozpoczeciapolisy'],
                    )
            if zapytanie['pojazd']:
                pojazd = zapytanie['pojazd']
                p = Pojazd.objects.create(
                        marka=pojazd['marka'],
                        model=pojazd['model'],
                        rocznik=pojazd['rocznik'],
                        )
                Zapytanie.objects.filter(id=z.id).update(pojazd=p.id)
    except TypeError:
        print ("ZAŁOŻENIE: wartość 'zapytanie' w pobieranym pliku musi być listą słowników")


    try:
        for odpowiedz in data['odpowiedz']:
            o = Odpowiedz.objects.create(
                    skladka=odpowiedz['skladka'],
                    czy_klient_szkodowy=odpowiedz['czyklientszkodowy'],
                    )
            if odpowiedz['pokrycia']:
                for pokrycie in odpowiedz['pokrycia']:
                    p = Pokrycie.objects.create(
                            nazwa=pokrycie['nazwapokrycia'],
                            ubezpieczenie_suma=pokrycie['sumaubezpieczenia'],
                            )
                    o.pokrycie_list.add(p)
                    o.save()
                    if pokrycie['zakres']:
                        p_zakres = pokrycie['zakres']
                        zakres = Zakres.objects.create(
                                amortyzacja=p_zakres['amortyzacja'],
                                dostepnosc_warunkowa=p_zakres['dostepnewarunkowo'],
                                )
                        Pokrycie.objects.filter(id=p.id).update(zakres=zakres.id)
    except TypeError:
        print ("ZAŁOŻENIE: wartość 'odpowiedz' w pobieranym pliku musi być listą słowników")

    # Closing file
    f.close()


import sqlite3
import pandas as pd

conn = sqlite3.connect('db.sqlite3')

print ('====================ZAPYTANIE====================')
sql_query_zapytanie = pd.read_sql_query (
        '''SELECT * FROM zapytanie_zapytanie''', 
        conn
        )

df = pd.DataFrame(sql_query_zapytanie, columns = [
    'zapytanie_id',
    'imie',
    'nazwisko',
    'regon',
    'urodzenie_data',
    'pojazd_id',
    'rozpoczecie_polisy_data',
    ]).rename(columns={
        'zapytanie_id': 'idzapytania',
        'urodzenie_data': 'dataurodzenia',
        'pojazd_id': 'pojazd',
        'rozpoczecie_polisy_data': 'datarozpoczeniapolisy',
        })
print (df)

print ('====================POJAZD====================')
sql_query_pojazd = pd.read_sql_query (
        '''SELECT * FROM pojazd_pojazd''', 
        conn
        )

df = pd.DataFrame(sql_query_pojazd, columns = [
    'marka',
    'model',
    'rocznik',
    ])
print (df)

print ('====================ODPOWIEDZ====================')
sql_query_odpowiedz = pd.read_sql_query (
        '''SELECT * FROM odpowiedz_odpowiedz''', 
        conn
        )

df = pd.DataFrame(sql_query_odpowiedz, columns = [
    'skladka',
    'pokrycie_list',
    'czy_klient_szkodowy',
    ]).rename(columns={
        'pokrycie_list': 'pokrycia',
        'czy_klient_szkodowy': 'czyklientszkodowy',
        })
print (df)

print ('====================POKRYCIE====================')
sql_query_pokrycie = pd.read_sql_query (
        '''SELECT * FROM pokrycie_pokrycie''', 
        conn
        )
df = pd.DataFrame(sql_query_pokrycie, columns = [
    'nazwa',
    'ubezpieczenie_suma',
    'zakres_id',
    ]).rename(columns={
        'nazwa': 'nazwapokrycia',
        'ubezpieczenie_suma': 'sumaubezpieczenia',
        'zakres_id': 'zakres',
        })
print (df)


print ('====================ZAKRES====================')
sql_query_zakres = pd.read_sql_query (
        '''SELECT * FROM zakres_zakres''', 
        conn
        )

df = pd.DataFrame(sql_query_zakres, columns = [
    'amortyzacja', 
    'dostepnosc_warunkowa'
    ]).rename(columns={
        'dostepnosc_warunkowa': 'dostepnewarunkowo',
        })
print (df)
