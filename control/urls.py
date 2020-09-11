from django.urls import path
from . import views

app_name = 'control'

urlpatterns =[
    path('', views.index, name='index'),
    path('discover/',views.discover, name='discover'),
    path('account_info/',views.account_info,name='account_info'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register,name='register'),
    path('account_info/make_profile/',views.make_profile,name='add_profile'),
]