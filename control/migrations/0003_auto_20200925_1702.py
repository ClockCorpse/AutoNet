# Generated by Django 3.1 on 2020-09-25 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0002_devicetemp'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='deviceType',
            field=models.CharField(default='cisco_ios', max_length=255),
        ),
        migrations.AddField(
            model_name='devicetemp',
            name='deviceType',
            field=models.CharField(default='cisco_ios', max_length=255),
        ),
    ]
