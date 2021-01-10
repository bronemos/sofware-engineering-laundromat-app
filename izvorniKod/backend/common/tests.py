import datetime

import pytz
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from common.models import User, Appointment, Machine, Laundry


class AccountTests(TestCase):
    def setUp(self):
        User.objects.create_user(JMBAG="1234567890", username='test', password='1Zaboraviti2', is_active=False)

    def test_unactivated_user_cant_login(self):
        """Izaziva grešku jer korisnik nije aktiviran"""
        response = self.client.post('/api/token-auth/', {'username': 'test', 'password': '1Zaboraviti2'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activated_user_can_login(self):
        """Rubni uvjet: može li se ulogirati odmah nakon što je potvrđen račun"""
        user = User.objects.filter(username='test').first()
        user.is_active = True
        user.save()
        response = self.client.post('/api/token-auth/', {'username': 'test', 'password': '1Zaboraviti2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AdminTests(TestCase):
    def setUp(self):
        User.objects.create_user(JMBAG="1234567890", username='test', password='1Zaboraviti2')
        User.objects.create_user(JMBAG="1234567899", username='admin', password='1Zaboraviti2', is_superuser=True, is_staff=True)

    def test_user_can_block_user(self):
        """Izaziva grešku jer korisnik nije admin"""
        user_id = User.objects.filter(username='test').first().id
        response = self.client.delete(f'/api/admin/{user_id}/delete_user/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_block_user(self):
        """Trebalo bi se smjeti kad je admin ulogiran"""
        user = User.objects.get(username='admin')
        client = APIClient()
        # client.login(username='admin', password='1Zaboraviti2')
        token = self.client.post('/api/token-auth/', {'username': 'admin', 'password': '1Zaboraviti2'}).data.get('token')
        # print(self.client.get('/api/account/logged_user_data/', headers={'Authorization': 'token ' + token}).data)
        user_id = User.objects.filter(username='test').first().id
        client.force_authenticate(user=user, token=token)
        response = client.delete(f'/api/admin/{user_id}/delete_user/')  # , headers={'Authorization': 'token' + token})
        # force_authenticate(response, user=user, token=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkerTests(TestCase):
    def setUp(self):
        User.objects.create_user(JMBAG="1234567890", username='test', password='1Zaboraviti2', baskets=1)
        User.objects.create_user(JMBAG="1234567899", username='admin', password='1Zaboraviti2', is_superuser=True, is_staff=True)

    def test_return_basket_non_worker(self):
        """Izaziva grešku jer korisnik nije zaposlenik"""
        user_id = User.objects.filter(username='test').first().id
        response = self.client.post(f'/api/admin/{user_id}/return_basket/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_return_basket_worker(self):
        """Ne izaziva grešku jer je korisnik zaposlenik"""
        user = User.objects.get(username='admin')
        client = APIClient()
        # client.login(username='admin', password='1Zaboraviti2')
        token = self.client.post('/api/token-auth/', {'username': 'admin', 'password': '1Zaboraviti2'}).data.get('token')
        # print(self.client.get('/api/account/logged_user_data/', headers={'Authorization': 'token ' + token}).data)
        user_id = User.objects.filter(username='test').first().id
        client.force_authenticate(user=user, token=token)
        response = client.post(f'/api/admin/{user_id}/return_basket/')  # , headers={'Authorization': 'token' + token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(username='test').first().baskets, 0)

    def test_return_basket_when_no_baskets_are_borrowed(self):
        """Provjera hoće li broj košara biti negativan"""
        user = User.objects.get(username='admin')
        client = APIClient()
        # client.login(username='admin', password='1Zaboraviti2')
        token = self.client.post('/api/token-auth/', {'username': 'admin', 'password': '1Zaboraviti2'}).data.get('token')
        # print(self.client.get('/api/account/logged_user_data/', headers={'Authorization': 'token ' + token}).data)
        user_id = User.objects.filter(username='test').first().id
        client.force_authenticate(user=user, token=token)
        response = client.post(f'/api/admin/{user_id}/return_basket/')  # , headers={'Authorization': 'token' + token})
        # force_authenticate(response, user=user, token=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.filter(username='test').first().baskets, 0)


class AppointmentTests(TestCase):
    def setUp(self):
        User.objects.create_user(JMBAG="1234567890", username='test', password='1Zaboraviti2')
        Machine.objects.create(type='washer')
        Laundry.objects.create(
            open_time=datetime.time(8, 0),
            close_time=datetime.time(20, 0),
            pause_start=datetime.time(10, 0),
            pause2_start=datetime.time(16, 0),
            drying_price=10,
            wash_price=10,
            date_changed=datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=1)
        )

    def test_unregistered_user_can_make_an_appointment(self):
        """Izaziva grešku jer korisnik nije ulogiran"""
        user_id = User.objects.filter(username='test').first().id
        response = self.client.post(
            f'/api/appointment/',
            {
                'machine': Machine.objects.first().id,
                'start': '2021-10-10T8:00Z',
                'paid': False
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_registered_user_can_make_an_appointment(self):
        """Trebalo bi se smjeti kad je korisnik ulogiran"""
        user = User.objects.get(username='test')
        client = APIClient()
        # client.login(username='admin', password='1Zaboraviti2')
        token = self.client.post('/api/token-auth/', {'username': 'admin', 'password': '1Zaboraviti2'}).data.get('token')
        # print(self.client.get('/api/account/logged_user_data/', headers={'Authorization': 'token ' + token}).data)
        user_id = User.objects.filter(username='test').first().id
        client.force_authenticate(user=user, token=token)
        response = client.post(
            f'/api/appointment/',
            {
                'machine': Machine.objects.first().id,
                'start': '2021-10-10T8:00Z',
                'paid': False
            }
        )  # , headers={'Authorization': 'token' + token})
        # force_authenticate(response, user=user, token=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
