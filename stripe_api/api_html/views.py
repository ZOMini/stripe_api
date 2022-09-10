from django.shortcuts import render


def success(request):
    template = 'api_html/success.html'
    context = {}
    return render(request, template, context)

def cancel(request):
    template = 'api_html/cancel.html'
    context = {}
    return render(request, template, context)

def buy_item(request):
    template = 'api_html/buy_item.html'
    context = {}
    return render(request, template, context)
