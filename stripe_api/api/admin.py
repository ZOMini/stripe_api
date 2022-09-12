from django.contrib import admin

from api.models import Discount, Item, Order, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'description', 'price', 'currency')
    search_fields = ('name', )
    empty_value_display = '-пусто-'
    list_filter = ('name',)


@admin.register(Discount)
class DiscontAdmin(admin.ModelAdmin):

    list_display = ('id', 'discont_unit', 'discont_link')
    search_fields = ('discont_unit', )
    empty_value_display = '-пусто-'
    list_filter = ('discont_unit',)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):

    list_display = ('id', 'tax_unit', 'tax_link')
    search_fields = ('tax_unit', )
    empty_value_display = '-пусто-'
    list_filter = ('tax_unit',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # В админке несколько товаров - зажав "ctr".
    list_display = ('id', 'get_items', 'discont', 'tax')

    def get_items(self, obj):
        return "\n".join([p.name for p in obj.items.all()])
