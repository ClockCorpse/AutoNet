from django.contrib import admin
from .models import Profile, Device, DeviceTemp, ExtendedUser, UserConfig
# Register your models here.

# admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(DeviceTemp)
admin.site.register(Profile)
admin.site.register(ExtendedUser)
admin.site.register(UserConfig)
