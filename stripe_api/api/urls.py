from django.contrib import admin
from django.urls import path

from api.views import buy_item, item_detail

app_name = 'api'

urlpatterns = [
    path('item/<str:id>/', item_detail, name='item_detail'),
    path('buy/<str:id>/', buy_item, name='buy_item'),
]
