from datetime import datetime

from django.contrib import auth
from django.contrib.auth import password_validation
from django.core.mail import send_mail

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny

from .models import User, Post, Laundry, Appointment, Card, Review
from .serializers import UserSerializer, PostSerializer, LaundrySerializer, AppointmentSerializer, CardSerializer, \
    ReviewSerializer, EmailSerializer
from rest_framework.response import Response


class OnlyFieldsSerializerMixin:
    def get_serializer(self, *args, **kwargs):
        kwargs['only_fields'] = self.only_fields
        return super().get_serializer(*args, **kwargs)


class AccountViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['only_fields'] = ['password', 'username', 'first_name', 'last_name', 'email', 'JMBAG']
            return super().get_serializer(*args, **kwargs)
        elif self.action == 'confirm' or self.action == 'logout':
            return None
        elif self.action == 'login':
            kwargs['only_fields'] = ['password', 'username']
            return super().get_serializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    permission_classes_by_action = {
        'confirm': [IsAdminUser],
        'logged_user_data': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'destroy': [IsAdminUser],
        'pending_users': [IsAdminUser],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create()
            user.is_active = False
            user.save()
            send_mail(
                'Potvrda registracije za aplikaciju Terminko!',
                f'Uputite se u praonicu veša s xicom kako bi zaposlenik mogao potvrditi vaš račun!',
                "noreply@somehost.local",
                [user.email]
            )
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], name='confirm')
    def confirm(self, request, pk=None):
        user = self.get_object()
        if user is not None and not user.is_active:
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['GET'], name='logged_user_data')
    def logged_user_data(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return Response(
                {'user': UserSerializer(user, only_fields=['username', 'first_name', 'last_name', 'email', 'negative_points',
                                                           'is_superuser', 'is_staff', 'JMBAG', 'id', 'card']).data},
                status=status.HTTP_200_OK
            )

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['GET'], name='pending_users')
    def pending_users(self, request, *args, **kwargs):
        return Response({'pending': UserSerializer(User.objects.filter(is_active=False),
                                                   only_fields=['first_name', 'last_name', 'JMBAG', 'id'],
                                                   many=True).data
                         })


class CardViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card = serializer.save()
        user = request.user
        user.card = card
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AdminViewSet(viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True, is_superuser=False)
    permission_classes = [IsAdminUser]

    permission_classes_by_action = {
        'list_workers': [IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        return UserSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create_worker_account':
            kwargs['only_fields'] = ['password', 'username', 'first_name', 'last_name', 'email', 'JMBAG', 'is_staff']
            return super().get_serializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    @action(detail=False, methods=['GET'], name='list_users')
    def list_users(self, request):
        return Response(
            UserSerializer(
                self.get_queryset().filter(is_staff=False),
                only_fields=['id', 'first_name', 'last_name', 'username', 'email', 'JMBAG', 'date_joined',
                             'negative_points'],
                many=True
            ).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['GET'], name='list_workers')
    def list_workers(self, request):
        return Response(
            UserSerializer(
                self.get_queryset().filter(is_staff=True),
                only_fields=['id', 'first_name', 'last_name', 'username', 'email', 'JMBAG', 'date_joined',
                             'negative_points'],
                many=True
            ).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['DELETE'], name='delete_user')
    def delete_user(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], name='create_worker_account')
    def create_worker_account(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create()
        user.is_staff = True
        user.save()
        send_mail(
            'Čestitamo na zaposlenju!!',
            f'Admin Vas je upravo dodao u aplikaciju terminko na funkciju zaposlenika. Vaši korisnički podaci za login '
            f'su: username: {user.username}, password: {request.data.get("password")}',
            "noreply@somehost.local",
            [user.email]
        )
        return Response(
            UserSerializer(
                user,
                only_fields=['id', 'first_name', 'last_name', 'username', 'email', 'JMBAG', 'date_joined']
            ).data,
            status=status.HTTP_201_CREATED
        )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LaundryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Laundry.objects.all()
    serializer_class = LaundrySerializer

    permission_classes_by_action = {
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'partial_update': [IsAdminUser],
        'list': [AllowAny],
        'future_laundry': [AllowAny],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def list(self, request, *args, **kwargs):
        return Response(
            LaundrySerializer(Laundry.objects.filter(date_changed__lte=datetime.now()).first()).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['GET'], name='future_laundry')
    def future_laundry(self, request):
        return Response(
            LaundrySerializer(Laundry.objects.filter(date_changed__gt=datetime.now()), many=True).data,
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        laundry_now = serializer.save()
        for laundry in Laundry.objects.filter(date_changed__gte=datetime.now()):
            laundry.pause_start = laundry_now.pause_start
            laundry.pause_end = laundry_now.pause_end
            laundry.wash_price = laundry_now.wash_price
            laundry.drying_price = laundry_now.drying_price
        return Response(serializer.data)


class AppointmentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = Appointment.objects.all()

    def get_serializer_class(self):
        if self.action == 'send_email':
            return EmailSerializer
        return AppointmentSerializer

    permission_classes = [IsAdminUser]
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'destroy': [IsAuthenticated],
        'logged_user_appointments': [IsAuthenticated]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=['POST'], name='send_email')
    def send_email(self, request, pk=None):
        appointment = self.get_object()
        email = appointment.user.email
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            send_mail(
                    'Poruka iz praonice!',
                    serializer.validated_data.get('text'),
                    "noreply@somehost.local",
                    [email]
                )
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], name='missed')
    def missed(self, request, pk=None):
        appointment = self.get_object()
        appointment.missed = True
        appointment.save()
        user = appointment.user
        user.negative_points = user.negative_points + 1
        user.save()
        send_mail(
            'Preskočen termin',
            f'Niste došli na rezervirani termin {appointment.start} te ste dobili negativan bod. Trenutno imate '
            f'{user.negative_points} negativnih bodova!',
            "noreply@somehost.local",
            [user.email]
        )
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], name='logged_user_appointments')
    def logged_user_appointments(self, request):
        return Response(self.get_serializer(Appointment.objects.filter(user__id=request.user.id), many=True).data)


class ReviewViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'list': [IsAdminUser],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
