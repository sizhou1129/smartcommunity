#coding:utf-8
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('login', handle_login, name='handle_login'),
    path('logout', handle_logout, name='handle_logout'),
    path('reginfo', handle_reginfo, name='handle_reginfo'),
    path('house', handle_house, name='handle_house'),
    path('fee', handle_fee, name='handle_fee'),
    path('feesetting/basic', handle_fee_basic, name='handle_fee_basic'),
    path('feesetting/special', handle_fee_special, name='handle_fee_special'),
    path('repair', handle_repair, name='handle_repair'),
    path('housemanager', handle_housemanager, name='handle_housemanager'),
    path('aroundservice', handle_aroundservice, name='handle_aroundservice')
]
