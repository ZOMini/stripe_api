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
