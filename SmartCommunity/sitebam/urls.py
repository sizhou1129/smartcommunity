#coding:utf-8
from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('', handle_test, name='handle_test'),
    path('login', handle_login, name='handle_login'),
    path('logout', handle_logout, name='handle_logout'),
    path('metadata', handle_metadata, name='handle_metadata'),
    path('community', handle_community, name='handle_community'),
    path('shop', handle_merchant, name='handle_merchant'),
    path('product', handle_product, name='handle_product'),
    path('adv', handle_adv, name='handle_adv'),
    path('index', handle_index, name='handle_index'),
    path('shop/commision', handle_commision, name='handle_commision')
]
