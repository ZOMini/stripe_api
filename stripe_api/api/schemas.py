from drf_yasg import openapi

ITEM_DETAIL = openapi.Parameter(
    'coupon',
    openapi.IN_QUERY,
    description='?coupon=sljEVntJ (8%) or ?coupon=9Sh6wF76 (16%)',
    type=openapi.TYPE_STRING,
    required=False,
    default='sljEVntJ')

ORDER_RESPONSE = openapi.Response(
    description="The order was successfully created",
    examples={
        "application/json": {
            "orderID": 1
        }
    }
)

ORDER_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'items': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER),
            description='list items id',
            default=[1, 2]),
        'discont': openapi.Schema(
            type=openapi.TYPE_STRING,
            default='sljEVntJ'),
        'tax': openapi.Schema(type=openapi.TYPE_STRING, default='20%'),
    },
    required=['items', ]
)
