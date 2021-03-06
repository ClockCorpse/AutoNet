# Generated by Django 3.1 on 2020-09-24 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceTemp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=255)),
                ('managementIP', models.GenericIPAddressField()),
                ('localPort', models.CharField(max_length=255)),
                ('remotePort', models.CharField(max_length=255)),
                ('platform', models.CharField(max_length=255)),
                ('softwareVersion', models.CharField(max_length=255)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
