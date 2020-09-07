from django.db import models
from django.contrib.auth.models import User,Permission

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    profileName = models.CharField(max_length=255)
    profilePassword = models.CharField(max_length=255)
    profileEnablePassword = models.CharField(max_length=255)

    def __str__(self):
        return User.USERNAME_FIELD + ' ' + self.pk

class Device(models.Model):
    user = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255)
    deviceIP = models.GenericIPAddressField()
    remotePort = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)

    def __str__(self):
        return self.hostname