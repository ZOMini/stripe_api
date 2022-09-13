import stripe
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from api.models import Item, Order
from api.serializers import OrderSerializer
from api.sub_view import generate_item, generate_line_items
from api.var import API_KEY, CANCEL_URL, SUCCESS_URL

stripe.api_key = API_KEY


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def item_detail(request, id):
    discont = request.query_params.get('coupon')
    item = get_object_or_404(Item, id=id)
    context = {'id': id, 'item': item, 'coupon': discont}
    return Response(data=context, template_name='api_html/buy_item_api.html')


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


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def order_create(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.create(serializer.validated_data)
    return Response(data={'orderID': data},
                    status=status.HTTP_201_CREATED)


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
