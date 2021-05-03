from django.urls import path
from . import views

app_name = 'control'

urlpatterns =[
    path('', views.index, name='index'),
    path('discover_devices/',views.discover_form, name='discover_devices'),
    path('discover/',views.discover,name='discover'),
    path('add_discovered',views.add_discovered,name='add_discovered'),
    path('account_info/',views.account_info,name='account_info'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register,name='register'),
    path('account_info/make_profile/',views.make_profile,name='add_profile'),
    path('account_info/<int:profile_id>/delete/',views.delete_profile,name='delete_profile'),
    path('account_info/<int:profile_id>/',views.update_profile_form,name='update_profile_form'),
    path('account_info/<int:profile_id>/update',views.change_profile,name='update_profile'),
    path('account_info/password/', views.change_password, name='change_password'),
    path('device_list/',views.diviceList,name='device_list'),
    path('device_list/remove',views.remove_device,name='remove_device'),
    path('device_detail/<int:device_id>/newIP',views.change_MgmtIP,name='updateIP'),
    path('device_detail/<int:device_id>/',views.deviceDetail,name='device_detail'),
    path('device_detail/update_interface/<int:device_id>/',views.getDeviceInfoAPI,name='updateInterface'),
    path('createUser/', views.addUserPage, name='createUserPage'),
    path('block/',views.block,name='block'),
    path('DSuserList/',views.DSUserList,name='DSUserList'),
    path('userList/deleteUser',views.removeUser,name='deleteUser'),
    path('userList/<int:user_id>/updateDSUser/',views.updateDSUser,name='updateDSUser'),
    path('addOU/',views.makeOU,name='addOU'),
    path('promoteDomain/',views.promoteDomain,name='promoteDomain'),
    path('findResult/',views.findUser,name='findUser'),
    path('addFile/',views.addCSVpage,name='addFile'),
    path('configure/',views.create_config,name='create_config'),
    path('device_list/manual_config', views.manual_config_form,name='manual_config_form'),
]