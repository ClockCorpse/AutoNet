from django.urls import path
from . import views

app_name = 'control'

urlpatterns =[
    path('', views.index, name='index'),
    path('discover/',views.discover_form, name='discover'),
    path('account_info/',views.account_info,name='account_info'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register,name='register'),
    path('account_info/make_profile/',views.make_profile,name='add_profile'),
    path('account_info/<int:profile_id>/delete/',views.delete_profile,name='delete_profile'),
    path('account_info/<int:profile_id>/',views.update_profile_form,name='update_profile_form'),
    path('account_info/<int:profile_id>/update',views.change_profile,name='update_profile'),
    path('account_info/password/', views.change_password, name='change_password'),
]