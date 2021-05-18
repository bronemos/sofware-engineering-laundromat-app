# Generated by Django 3.1.2 on 2020-11-05 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Praonica',
            fields=[
                ('datum', models.DateField(editable=False, primary_key=True, serialize=False)),
                ('pocetakRada', models.DateTimeField()),
                ('krajRada', models.DateTimeField()),
                ('pauza', models.DateTimeField()),
                ('pranjeCijena', models.FloatField()),
                ('susenjeCijena', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Uredaj',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ime', models.CharField(max_length=255)),
                ('vrsta', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='JMABG',
            field=models.CharField(default='xxx', max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ime',
            field=models.CharField(default='xxx', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='kreditnaKartica',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='lozinka',
            field=models.CharField(default='xxx', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='negativniBodovi',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='prezime',
            field=models.CharField(default='xxx', max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='zaposlenik',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(default='xxx', max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name='RezerviraniTermin',
            fields=[
                ('termin', models.TimeField(editable=False, primary_key=True, serialize=False)),
                ('cijena', models.FloatField()),
                ('biljeska', models.TextField(blank=True, null=True)),
                ('placeno', models.BooleanField()),
                ('posudjenaKosara', models.BooleanField()),
                ('idKorisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rezerviranitermin_requests_created1', to=settings.AUTH_USER_MODEL)),
                ('idUredaj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.uredaj')),
                ('idZaposlenik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rezerviranitermin_requests_created2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recenzije',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('recenzija', models.TextField(blank=True, null=True)),
                ('ocjena', models.IntegerField()),
                ('idKorisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recenzije_requests_created1', to=settings.AUTH_USER_MODEL)),
                ('idZaposlenik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recenzije_requests_created2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Objava',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slika', models.ImageField(blank=True, null=True, upload_to='')),
                ('tekst', models.TextField()),
                ('datumObjave', models.DateField()),
                ('LF', models.BooleanField()),
                ('idZaposlenik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objava_requests_created1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]