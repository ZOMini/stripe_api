from django.contrib import admin
from django.urls import path

from api.views import (
    buy_item,
    item_detail,
    order_buy,
    order_create,
    order_html
)

app_name = 'api'

urlpatterns = [
    path('item/<str:id>/', item_detail, name='item_detail'),
    path('buy/<str:id>/', buy_item, name='buy_item'),
    path('order_create/', order_create, name='order_create'),
    path('order_html/<str:id>/', order_html, name='order_html'),
    path('order_buy/<str:id>/', order_buy, name='order_buy'),
]
