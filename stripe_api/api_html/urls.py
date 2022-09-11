from api_html.views import cancel, success
from django.urls import path

app_name = 'api_html'

urlpatterns = [
    path('success', success, name='buy_success'),
    path('cancel', cancel, name='buy_cancel'),
]
