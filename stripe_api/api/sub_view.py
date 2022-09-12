from api.var import TAX20


def generate_line_items(order, items):
    line_items, items_currency = [], set()
    if order.tax is not None:
        tax = order.tax.tax_link
    else:
        tax = TAX20
    for item in items:
        items_currency.add(item.currency)
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'product_data': {'name': item.name, },
                'unit_amount': int(item.price) * 100,
            },
            'quantity': 1,
            'tax_rates': [tax],
        })
    if len(items_currency) > 1:
        valid = False
    else:
        valid = True
    return line_items, valid
