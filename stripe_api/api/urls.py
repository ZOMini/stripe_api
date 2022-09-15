from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views import (
    buy_item,
    item_detail,
    order_buy,
    order_create,
    order_html
)

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="Stripe API",
        default_version='v1',
        description="Stripe API testwork",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(url="https://github.com/ZOMini/stripe_api"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('item/<str:id>/', item_detail, name='item_detail'),
    path('buy/<str:id>/', buy_item, name='buy_item'),
    path('order_create/', order_create, name='order_create'),
    path('order_html/<str:id>/', order_html, name='order_html'),
    path('order_buy/<str:id>/', order_buy, name='order_buy'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
