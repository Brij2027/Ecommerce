# Generated by Django 3.0.7 on 2020-07-11 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_auto_20200711_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='totp',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
