import stripe
from django.shortcuts import get_object_or_404, redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

import api.schemas as sch
from api.models import Item, Order
from api.serializers import OrderSerializer
from api.sub_view import generate_item, generate_line_items
from api.var import API_KEY, CANCEL_URL, SUCCESS_URL

stripe.api_key = API_KEY


@swagger_auto_schema(
    method='get',
    manual_parameters=[sch.ITEM_DETAIL],
    operation_description='HTML - individual product purchase page.',
    tags=['Operations with individual goods'],
    responses={200: 'HTML page', 404: 'Not found'})
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def item_detail(request, id):
    discont = request.query_params.get('coupon')
    item = get_object_or_404(Item, id=id)
    context = {'id': id, 'item': item, 'coupon': discont}
    return Response(data=context, template_name='api_html/buy_item_api.html')


@swagger_auto_schema(
    method='get',
    manual_parameters=[sch.ITEM_DETAIL],
    operation_description='API redirect.',
    tags=['Operations with individual goods'],
    responses={303: 'Redirecting to the purchase page.', 404: 'Not found'})
@api_view(['GET'])
def buy_item(request, id):
    discont = request.query_params.get('coupon')
    if discont == 'None':
        discont = []
    item = get_object_or_404(Item, id=id)
    item_list = []
    item_list.append(generate_item(item))
    session = stripe.checkout.Session.create(
        line_items=item_list,
        mode='payment',
        discounts=[{'coupon': discont}],
        success_url=SUCCESS_URL,
        cancel_url=CANCEL_URL,
    )
    return redirect(session.url)


@swagger_auto_schema(
    method='post',
    operation_description='API post order.',
    tags=['Operations with order'],
    request_body=sch.ORDER_BODY,
    responses={201: sch.ORDER_RESPONSE,
               400: 'ValidationError',
               404: 'Not found'})
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def order_create(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.create(serializer.validated_data)
    return Response(data={'orderID': data},
                    status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='get',
    operation_description='HTML - Order purchase page.',
    tags=['Operations with order'],
    responses={200: 'HTML page', 404: 'Not found'})
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def order_html(request, id):
    order = get_object_or_404(Order, id=id)
    items = Item.objects.filter(order=id)
    summ = 0
    for item in items:
        summ += item.price
    context = {'id': id, 'order': order, 'items': items, 'summ': summ}
    return Response(data=context, template_name='api_html/order_api.html')


@swagger_auto_schema(
    method='get',
    operation_description='API redirect.',
    tags=['Operations with order'],
    responses={303: 'Redirecting to the purchase page.', 404: 'Not found'})
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def order_buy(request, id):
    try:
        order = Order.objects.get(id=id)
        items = Item.objects.filter(order=id)
    except Exception as e:
        return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)
    line_items, valid = generate_line_items(order, items)
    if not valid:
        return Response({'error': 'Товары в заказе имеют разные валюты.'},
                        status=status.HTTP_409_CONFLICT)
    if order.discont is None:
        discont = []
    else:
        discont = [{'coupon': order.discont.discont_link}]
    session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        discounts=discont,
        success_url=SUCCESS_URL,
        cancel_url=CANCEL_URL,
    )
    return redirect(session.url)
