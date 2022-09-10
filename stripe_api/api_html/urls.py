from api_html.views import buy_item, cancel, success
from django.contrib import admin
from django.urls import path

app_name = 'api_html'

urlpatterns = [
    path('success', success, name='buy_success'),
    path('cancel', cancel ,name='buy_cancel'),
    path('buy_item', buy_item ,name='buy_item'),
]
