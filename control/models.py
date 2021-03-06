from django.db import models
from django.contrib.auth.models import User,Permission

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    profileName = models.CharField(max_length=255)
    profilePassword = models.CharField(max_length=255)
    profileEnablePassword = models.CharField(max_length=255)

    def __str__(self):
        return self.profileName

class Device(models.Model):
    user = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255)
    managementIP = models.GenericIPAddressField()
    localPort = models.CharField(max_length=255)
    remotePort = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    softwareVersion = models.CharField(max_length=255)
    deviceType = models.CharField(max_length=255,default='cisco_ios')
    
    def __str__(self):
        return self.hostname

class DeviceTemp(models.Model):
    user = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255)
    managementIP = models.GenericIPAddressField()
    localPort = models.CharField(max_length=255)
    remotePort = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    softwareVersion = models.CharField(max_length=255)
    deviceType = models.CharField(max_length=255, default='cisco_ios')

    def __str__(self):
        return self.hostname