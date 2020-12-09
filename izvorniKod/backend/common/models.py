import uuid

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = 'localhost:3000/reset-password?token={}'.format(reset_password_token.key)

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    JMBAG = models.CharField(null=False, unique=True, blank=False, max_length=10, default='xxx')
    cart_number = models.IntegerField(null=False, blank=False, default=0)
    negative_points = models.IntegerField(null=False, blank=False, default=0)


class WashDay(models.Model):
    date = models.DateField(unique=True, editable=False)
    open_time = models.TimeField(null=False, blank=False)
    close_time = models.TimeField(null=False, blank=False)
    pause_start = models.TimeField(null=False, blank=False)
    pause_end = models.TimeField(null=False, blank=False)
    wash_price = models.FloatField(null=False, blank=False)
    drying_price = models.FloatField(null=False, blank=False)


class Machine(models.Model):
    type = models.CharField(max_length=10, choices=[('washer', 'washer'), ('dryer', 'dryer')])


class Appointment(models.Model):
    time = models.DateField(unique=True, editable=False)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    price = models.FloatField(null=False, blank=False)
    note = models.TextField(null=True, blank=True)
    paid = models.BooleanField(null=False, blank=False)
    basket_taken = models.BooleanField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_worked')


class Post(models.Model):
    photo = models.ImageField(upload_to='images/', null=True)
    text = models.TextField(null=False, blank=False)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=[('lost', 'lost'), ('job', 'job')], default='lost')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recension_written')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recension')
    text = models.TextField(null=True, blank=True)
    grade = models.IntegerField(null=False, blank=False)
