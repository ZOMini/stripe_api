from django.db import models


class Item(models.Model):
    name = models.CharField('Имя товара', max_length=255, unique=True, blank=False)
    description = models.CharField('Описание товара', max_length=255)
    price = models.FloatField('Цена товара', blank=False)
    currency = models.CharField('Валюта',
                                max_length=3,
                                choices=[('usd', 'usd'), ('eur', 'eur')],
                                default='usd')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        default_related_name = 'Item'

    def __str__(self):
        return self.name


class Discount(models.Model):
    discont_unit = models.CharField('Скидка', max_length=255)
    discont_link = models.CharField('Ссылка Stripe', max_length=255)

    class Meta:
        verbose_name = 'Дисконт'
        verbose_name_plural = 'Дисконты'
        default_related_name = 'DiscontOrder'

    def __str__(self):
        return self.discont_unit

    def __repr__(self) -> str:
        return self.id


class Tax(models.Model):
    tax_unit = models.CharField('Налог', max_length=255)
    tax_link = models.CharField('Ссылка Stripe', max_length=255)

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'
        default_related_name = 'TaxOrder'

    def __str__(self):
        return self.tax_link

    def __repr__(self) -> str:
        return self.id


class Order(models.Model):
    discont = models.ForeignKey(
        Discount,
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name='Дисконт',
        help_text='Выберите дисконт для добавления в заказ',
        null=True,
        blank=True)
    tax = models.ForeignKey(
        Tax,
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name='Налог',
        help_text='Выберите налог для добавления в заказ',
        null=True,
        blank=True)
    items = models.ManyToManyField(
        Item,
        related_name='order',
        verbose_name='Заказ товаров.',
        help_text='Выберите товар.(В админке несколько товаров через - "Ctr")')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        default_related_name = 'Order'

    def __str__(self):
        return str(self.id)
