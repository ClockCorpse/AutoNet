from django.contrib import admin
from .models import Profile, Device, DeviceTemp
# Register your models here.

# admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(DeviceTemp)