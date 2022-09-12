import stripe
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import (
    BrowsableAPIRenderer,
    JSONRenderer,
    TemplateHTMLRenderer
)
from rest_framework.response import Response

from api.models import Discount, Item, Order, Tax
from api.sub_view import generate_line_items
from api.var import API_KEY, CANCEL_URL, SUCCESS_URL, TAX20

stripe.api_key = API_KEY

@api_view(['GET'])
@renderer_classes([BrowsableAPIRenderer])
def item_detail(request, id):
    discont = request.query_params.get('coupon')
    item = get_object_or_404(Item, id=id)
    context = {'id': id, 'item': item, 'coupon': discont}
    return Response(data=context, template_name='api_html/buy_item_api.html')


@api_view(['GET'])
def buy_item(request, id):
    discont = request.query_params.get('coupon')
    if discont == 'None': discont = []
    item = get_object_or_404(Item, id=id)
    session = stripe.checkout.Session.create(
        line_items=[{
        'price_data': {
            'currency': item.currency,
            'product_data': {
            'name': item.name,
            },
            'unit_amount': int(item.price*100),
        },
        'quantity': 1,
        'tax_rates': [TAX20],
        }],
        mode='payment',
        discounts=[{'coupon': discont,}],
        success_url=SUCCESS_URL,
        cancel_url=CANCEL_URL,
    )
    return redirect(session.url)
    


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def order_create(request):
    try: discont = Discount.objects.get(
        discont_link = request.data.get('discont'))
    except: discont = None
    try: tax = Tax.objects.get(tax_unit = request.data.get('tax'))
    except: tax = Tax.objects.get(tax_unit = 'tax20')
    items = request.data.get('items')
    if items is None:
        return Response({'error': '"items" is empty'},
                        status=status.HTTP_404_NOT_FOUND)
    items_list, items_currency = [], set()
    for item in items:
        item = get_object_or_404(Item, id=item)
        items_currency.add(item.currency)
        items_list.append(item)
    if len(items_currency)>1:
        return Response({'error': 'Товары в заказе имеют разные валюты.'},
                        status=status.HTTP_409_CONFLICT)
    try:
        order = Order.objects.create(discont=discont,
                                     tax=tax,)
        order.items.set(items_list)
    except Exception as e:
        return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)
    return Response(data={'orderID': order.id},
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
    else: discont = [{'coupon': order.discont.discont_link}]
    session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        discounts=discont,
        success_url=SUCCESS_URL,
        cancel_url=CANCEL_URL,
    )
    return redirect(session.url)
