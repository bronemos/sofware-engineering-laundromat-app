import random
import uuid
import datetime
import pytz
from datetime import datetime, timedelta, timezone

from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
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


class Card(models.Model):
    cc_number = CardNumberField()
    cc_expiry = CardExpiryField()
    cc_code = SecurityCodeField()


def random_string():
    return str(random.randint(10000, 99999))


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    JMBAG = models.CharField(null=False, unique=True, blank=False, max_length=10, default=random_string)
    card = models.OneToOneField(Card, null=True, blank=True, on_delete=models.SET_NULL)
    negative_points = models.IntegerField(null=False, blank=False, default=0)
    baskets = models.IntegerField(null=True, blank=True, default=0)


def return_date_changed():
    now = datetime.now()
    return now + timedelta(days=15)


class Laundry(models.Model):
    date_changed = models.DateTimeField(default=return_date_changed, blank=True)
    open_time = models.TimeField(null=False, blank=False)
    close_time = models.TimeField(null=False, blank=False)
    middle = models.TimeField(null=True, blank=True)
    pause_start = models.TimeField(null=False, blank=False)
    pause_end = models.TimeField(null=True, blank=True)
    pause2_start = models.TimeField(null=False, blank=False)
    pause2_end = models.TimeField(null=True, blank=True)
    wash_price = models.FloatField(null=False, blank=False)
    drying_price = models.FloatField(null=False, blank=False)
    first_shift_worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shift', null=True)
    second_shift_worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shift_2', null=True)

    class Meta:
        ordering = ['-date_changed']

    def add_mins(self, tm, min):
        fulldate = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        fulldate = fulldate + timedelta(minutes=min)
        return fulldate.time()

    def save(self, *args, **kwargs):
        if self.pause_start is not None:
            self.pause_end = self.add_mins(self.pause_start, 30)
        if self.pause2_start is not None:
            self.pause2_end = self.add_mins(self.pause2_start, 30)
        self.middle = self.add_mins(
            self.open_time,
            (self.close_time.hour * 60 + self.close_time.minute - self.open_time.hour * 60 - self.open_time.minute) / 2
        )
        super(Laundry, self).save(*args, **kwargs)


class Machine(models.Model):
    type = models.CharField(max_length=10, choices=[('washer', 'washer'), ('dryer', 'dryer')])


class Appointment(models.Model):
    start = models.DateTimeField(null=False, blank=False)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    price = models.FloatField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    paid = models.BooleanField(null=False, blank=False)
    basket_taken = models.BooleanField(null=True, default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_worked', blank=True,
                                 null=True)
    missed = models.BooleanField(default=False, blank=True)

    def save(self, *args, **kwargs):
        if self.machine.type == 'washer':
            self.price = Laundry.objects.filter(date_changed__lte=datetime.now()).first().wash_price
        else:
            self.price = Laundry.objects.filter(date_changed__lte=datetime.now()).first().drying_price
        super(Appointment, self).save(*args, **kwargs)

    def delete(self):
        utc = pytz.UTC
        if utc.localize(datetime.now() + timedelta(hours=3)) >= self.start:
            user = self.user
            user.negative_points += 1
            user.save()
        super(Appointment, self).delete()

    class Meta:
        ordering = ['-start']


class Post(models.Model):
    photo = models.ImageField(upload_to='images/', null=True)
    text = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=[('lost', 'lost'), ('job', 'job')], default='lost')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')

    class Meta:
        ordering = ['-date']


class Review(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='review', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_written')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    text = models.TextField(null=True, blank=True)
    grade = IntegerRangeField(null=False, blank=False, min_value=1, max_value=5)
