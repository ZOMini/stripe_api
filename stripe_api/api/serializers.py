from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import Discount, Item, Order, Tax


class OrderSerializer(serializers.Serializer):
    items = serializers.ListField()
    discont = serializers.CharField(required=False, )
    tax = serializers.CharField(required=False)

    def validate_items(self, value):
        if len(value) == 0:
            raise serializers.ValidationError('Товары в заказе отсутствуют.')
        currency = set()
        for item in value:
            item = get_object_or_404(Item, id=item)
            currency.add(item.currency)
        if len(currency) > 1:
            raise serializers.ValidationError('Товары в заказе имеют разные валюты.')
        return value

    def validate(self, data):
        if 'discont' not in data:
            data['discont'] = None
        else:
            discont = get_object_or_404(
                Discount,
                discont_link=data['discont']
            )
            data['discont'] = discont.id
        if 'tax' not in data:
            tax = Tax.objects.get(tax_unit='20%')
            data['tax'] = tax.id
        else:
            tax = get_object_or_404(Tax, tax_unit=data['tax'])
            data['tax'] = tax.id
        return data

    def create(self, validated_data):
        tax = validated_data.get('tax')
        tax = Tax.objects.get(id=tax)
        discont = validated_data.get('discont')
        if discont is not None:
            discont = Discount.objects.get(id=discont)
        items = validated_data.get('items')
        items_list = []
        for item in items:
            item = Item.objects.get(id=item)
            items_list.append(item)
        order = Order.objects.create(tax=tax, discont=discont)
        order.items.set(items_list)
        return order.id
