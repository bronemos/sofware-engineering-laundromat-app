import uuid

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)

    send_mail(
        # title:
        "Promijena lozinke za Terminko!",
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ime = models.CharField(null=False, blank=False, max_length=255, default='xxx')
    prezime = models.CharField(null=False, blank=False, max_length=255, default='xxx')
    JMABG = models.CharField(null=False, unique=True, blank=False, max_length=10, default='xxx')
    lozinka = models.CharField(null=False, blank=False, max_length=255, default='xxx')
    email = models.CharField(null=False, unique=True, blank=False, max_length=255, default='xxx')
    zaposlenik = models.BooleanField(null=False, blank=False, default=False)
    kreditnaKartica = models.IntegerField(null=False, blank=False, default=0)
    negativniBodovi = models.IntegerField(null=False, blank=False, default=0)

class Praonica(models.Model):
    datum = models.DateField(primary_key=True, editable=False)
    pocetakRada = models.DateTimeField(null=False, blank=False)
    krajRada = models.DateTimeField(null=False, blank=False)
    pauza = models.DateTimeField(null=False, blank=False)
    pranjeCijena = models.FloatField(null=False, blank=False)
    susenjeCijena = models.FloatField(null=False, blank=False)

class Uredaj(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ime = models.CharField(null=False, blank=False, max_length=255)
    vrsta = models.BooleanField(null=False, blank=False)

class RezerviraniTermin(models.Model):
    termin = models.TimeField(primary_key=True, editable=False)
    idUredaj = models.ForeignKey(Uredaj, on_delete=models.CASCADE)
    cijena = models.FloatField(null=False, blank=False)
    biljeska = models.TextField(null=True, blank=True)
    placeno = models.BooleanField(null=False, blank=False)
    posudjenaKosara = models.BooleanField(null=False, blank=False)
    idKorisnik =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created1')
    idZaposlenik =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created2')

class Objava(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slika = models.ImageField(null=True, blank=True)
    tekst = models.TextField(null=False, blank=False)
    datumObjave = models.DateField(null=False, blank=False)
    LF = models.BooleanField(null=False, blank=False)
    idZaposlenik = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_requests_created1')

class Recenzije(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idKorisnik = models.ForeignKey(User, on_delete=models.CASCADE , related_name='%(class)s_requests_created1')
    idZaposlenik = models.ForeignKey(User, on_delete=models.CASCADE , related_name='%(class)s_requests_created2')
    recenzija = models.TextField(null=True, blank=True)
    ocjena = models.IntegerField(null=False, blank=False)
