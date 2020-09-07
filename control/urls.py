from django.urls import path
from . import views

app_name = 'control'

urlpatterns =[
    path('', views.index, name='index'),
    path('discover/',views.discover, name='discover'),
    path('account_info/',views.account_info,name='account_info'),
]