import uuid
from datetime import datetime

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


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    JMBAG = models.CharField(null=False, unique=True, blank=False, max_length=10, default='xxx')
    cart_number = models.IntegerField(null=False, blank=False, default=0)
    negative_points = models.IntegerField(null=False, blank=False, default=0)


class Laundry(models.Model):
    date_changed = models.DateTimeField(auto_now_add=True, blank=True)
    open_time = models.TimeField(null=False, blank=False)
    close_time = models.TimeField(null=False, blank=False)
    pause_start = models.TimeField(null=False, blank=False)
    pause_end = models.TimeField(null=False, blank=False)
    wash_price = models.FloatField(null=False, blank=False)
    drying_price = models.FloatField(null=False, blank=False)

    class Meta:
        ordering = ['-date_changed']


class Machine(models.Model):
    type = models.CharField(max_length=10, choices=[('washer', 'washer'), ('dryer', 'dryer')])


class Appointment(models.Model):
    start_time = models.DateField(null=False, editable=False, blank=True, default=datetime.now)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    paid = models.BooleanField(null=False, blank=False)
    basket_taken = models.BooleanField(null=True, default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_worked', blank=True,
                                 null=True)

    def save(self, *args, **kwargs):
        if self.machine.type == 'washer':
            self.price = Laundry.objects.all().first().wash_price
        else:
            self.price = Laundry.objects.all().first().drying_price
        super(Appointment, self).save(*args, **kwargs)


class Post(models.Model):
    photo = models.ImageField(upload_to='images/', null=True)
    text = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=[('lost', 'lost'), ('job', 'job')], default='lost')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')

    class Meta:
        ordering = ['-date']


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recension_written')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recension')
    text = models.TextField(null=True, blank=True)
    grade = IntegerRangeField(null=False, blank=False, min_value=1, max_value=5)
