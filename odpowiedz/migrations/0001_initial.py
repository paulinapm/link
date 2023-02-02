# Generated by Django 3.2.15 on 2023-02-01 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pokrycie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Odpowiedz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skladka', models.DecimalField(decimal_places=2, max_digits=5)),
                ('czy_klient_szkodowy', models.BooleanField()),
                ('pokrycie_list', models.ManyToManyField(to='pokrycie.Pokrycie')),
            ],
        ),
    ]