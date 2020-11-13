# Generated by Django 3.1.2 on 2020-11-07 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20201105_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(editable=False, unique=True)),
                ('price', models.FloatField()),
                ('note', models.TextField(blank=True, null=True)),
                ('paid', models.BooleanField()),
                ('basket_taken', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.BooleanField(choices=[('washer', 'washer'), ('dryer', 'dryer')])),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('text', models.TextField()),
                ('date', models.DateField()),
                ('LF', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Recension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('grade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WashDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(editable=False, unique=True)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('pause_start', models.TimeField()),
                ('pause_end', models.TimeField()),
                ('wash_price', models.FloatField()),
                ('drying_price', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='objava',
            name='idZaposlenik',
        ),
        migrations.DeleteModel(
            name='Praonica',
        ),
        migrations.RemoveField(
            model_name='recenzije',
            name='idKorisnik',
        ),
        migrations.RemoveField(
            model_name='recenzije',
            name='idZaposlenik',
        ),
        migrations.RemoveField(
            model_name='rezerviranitermin',
            name='idKorisnik',
        ),
        migrations.RemoveField(
            model_name='rezerviranitermin',
            name='idUredaj',
        ),
        migrations.RemoveField(
            model_name='rezerviranitermin',
            name='idZaposlenik',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='kreditnaKartica',
            new_name='cart_number',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='negativniBodovi',
            new_name='negative_points',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ime',
        ),
        migrations.RemoveField(
            model_name='user',
            name='lozinka',
        ),
        migrations.RemoveField(
            model_name='user',
            name='prezime',
        ),
        migrations.RemoveField(
            model_name='user',
            name='zaposlenik',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.DeleteModel(
            name='Objava',
        ),
        migrations.DeleteModel(
            name='Recenzije',
        ),
        migrations.DeleteModel(
            name='RezerviraniTermin',
        ),
        migrations.DeleteModel(
            name='Uredaj',
        ),
        migrations.AddField(
            model_name='recension',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recension', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recension',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recension_written', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_worked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointment',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.machine'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to=settings.AUTH_USER_MODEL),
        ),
    ]