# Generated by Django 3.0.7 on 2020-07-11 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_auto_20200711_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='totp',
            field=models.IntegerField(blank=True),
        ),
    ]
