from django.shortcuts import get_object_or_404, render

from api.models import Item


def success(request):
    template = 'api_html/success.html'
    context = {}
    return render(request, template, context)

def cancel(request):
    template = 'api_html/cancel.html'
    context = {}
    return render(request, template, context)

def buy_item(request, id):
    template = 'api_html/buy_item.html'
    item = get_object_or_404(Item, id=id)
    context = {'id': id, 'item': item}
    return render(request, template, context)
