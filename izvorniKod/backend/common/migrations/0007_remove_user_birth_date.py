# Generated by Django 3.1.2 on 2020-11-08 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20201107_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='birth_date',
        ),
    ]
