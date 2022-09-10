import stripe
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

stripe.api_key = 'sk_test_51LgS9QGebgXU6S1ABxDT3Yj9r2BVJpZlYX8CK4b6f0SkapxkZMN3RRl76MjvNXgtMvTtpy89fYKMjsIMfj7RTBhH00ekjnhFhH'

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def item_detail(request, id):
    context = {'id':id}
    return Response(data=context, template_name='api_html/buy_item.html')
    # return redirect('http://127.0.0.1:8000/html/buy_item')


@api_view(['GET'])
# @renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def buy_item(request, *args, **kwargs):
    session = stripe.checkout.Session.create(
        line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
            'name': 'T-shirt',
            },
            'unit_amount': 2000,
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/html/success',
        cancel_url='http://127.0.0.1:8000/html/cancel',
    )

    return redirect(session.url)
