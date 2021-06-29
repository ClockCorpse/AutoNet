from django.urls import path
from . import views

app_name = 'control'

urlpatterns = [
    path('', views.index, name='index'),
    path('discover_devices/', views.discover_form, name='discover_devices'),
    path('discover/', views.discover, name='discover'),
    path('add_discovered', views.add_discovered, name='add_discovered'),
    path('account_info/', views.account_info, name='account_info'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('account_info/make_profile/', views.make_profile, name='add_profile'),
    path('account_info/make_profile/set_nag_server', views.set_nagios_server, name='set_nag'),
    path('account_info/make_profile/make_SNMPRead', views.create_snmp_read_cred, name='make_SNMPRead'),
    path('account_info/make_profile/make_SNMPWrite', views.create_snmp_write_cred, name='make_SNMPWrite'),
    path('account_info/<int:profile_id>/delete/', views.delete_profile, name='delete_profile'),
    path('account_info/<int:RO_id>/delete/SNMPRead/', views.delete_ROString, name='delete_ROString'),
    path('account_info/<int:RW_id>/delete/SNMPWrite/', views.delete_RWString, name='delete_RWString'),
    path('account_info/profile/<int:profile_id>/', views.update_profile_form, name='update_profile_form'),
    path('account_info/SNMPRead/<int:RO_id>/', views.update_ROString_form, name='update_SNMPRead_form'),
    path('account_info/SNMPWrite/<int:RW_id>/', views.update_RWString_form, name='update_SNMPWrite_form'),
    path('account_info/profile/update/<int:profile_id>/', views.change_profile, name='update_profile'),  # aaa
    path('account_info/SNMPRead/update/<int:RO_id>/', views.change_ROString, name='update_SNMPRead'),  # aaa
    path('account_info/SNMPWrite/update/<int:RW_id>/', views.change_RWString, name='update_SNMPWrite'),  # aaa
    path('account_info/password/', views.change_password, name='change_password'),
    path('device_list/', views.diviceList, name='device_list'),
    path('device_list/remove', views.remove_device, name='remove_device'),
    path('device_detail/<int:device_id>/newIP', views.change_MgmtIP, name='updateIP'),
    path('device_detail/<int:device_id>/', views.deviceDetail, name='device_detail'),
    path('device_detail/update_interface/<int:device_id>/', views.getDeviceInfoAPI, name='updateInterface'),
    path('createUser/', views.addUserPage, name='createUserPage'),
    path('block/', views.block, name='block'),
    path('DSuserList/', views.DSUserList, name='DSUserList'),
    path('userList/deleteUser', views.removeUser, name='deleteUser'),
    path('userList/<int:user_id>/updateDSUser/', views.updateDSUser, name='updateDSUser'),
    path('addOU/', views.makeOU, name='addOU'),
    path('promoteDomain/', views.promoteDomain, name='promoteDomain'),
    path('findResult/', views.findUser, name='findUser'),
    path('addFile/', views.addCSVpage, name='addFile'),
    path('configure/', views.create_config, name='create_config'),
    path('configure/<int:config_id>/get', views.get_config, name='get_config'),
    path('configure/delete', views.delete_config, name='delete_config'),
    path('device_list/manual_config', views.manual_config_form, name='manual_config_form'),
    path('device_detail/<int:deviceID>/<int:interfaceID>/keepAlive', views.toggle_keepAlive, name='keepAlive'),
    path('device_detail/<int:device_id>/get_running', views.getDeviceRunningConfig, name='get_running'),
    path('device_detail/<int:device_id>/get_startup', views.getDeviceStartupConfig, name='get_startup'),
    path('base_info', views.host_info_API, name='base_info'),
    path('host_usage_info', views.host_monitor_API, name='usage_info'),
    path('device_detail/<int:device_id>/get_usage', views.device_monitor_API, name='device_usage_info'),
    
    path('traceroute', views.traceroute_page, name='traceroute_page'),
    path('traceroute_return', views.traceroute, name='traceroute'),
    path('device_detail/<int:device_id>/get_routing_table', views.routingTableAPI, name='get_routing_table'),

]
