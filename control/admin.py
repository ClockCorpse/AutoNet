from django.contrib import admin
from .models import Profile, Device, DeviceTemp, DeviceInterface, ExtendedUser, UserConfig,ROCommunityString,RWCommunityString,NagiosServer
# Register your models here.

# admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(DeviceTemp)
admin.site.register(Profile)
admin.site.register(ExtendedUser)
admin.site.register(UserConfig)
admin.site.register(NagiosServer)
admin.site.register(DeviceInterface)
admin.site.register(ROCommunityString)
admin.site.register(RWCommunityString)
