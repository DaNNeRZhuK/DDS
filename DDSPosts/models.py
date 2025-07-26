"""
Модели для приложения.

Содержит классы:
- Status: Статус транзакции
- Type: Тип операции
- Category: Категория, привязанная к типу
- Subcategory: Подкатегория, привязанная к категории
- Transaction: Финансовая операция, привязанная к типу -> категории -> подкатегории
"""

from django.db import models
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey


class Status(models.Model):
    """Статус транзакции"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Статус')

    def __str__(self):
        return self.name


class Type(models.Model):
    """Тип операции"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Тип операции'
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    """Категория, связанная с типом операции"""
    name = models.CharField(
        max_length=100,
        verbose_name='Категория'
    )

    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип операции'
    )

    class Meta:
        unique_together = ('name', 'type')  # Категория уникальна в пределах типа

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Подкатегория, связанная с категорией"""
    name = models.CharField(
        max_length=100,
        verbose_name='Подкатегория'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    class Meta:
        unique_together = ('name', 'category')  # Подкатегория уникальна в пределах категории

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Основная модель"""

    date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания поста'
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )

    operation = models.ForeignKey(
        Type,
        on_delete=models.PROTECT,
        verbose_name='Тип операции'
    )

    category = ChainedForeignKey(
        Category,
        chained_field='operation',            # зависит от выбранного типа
        chained_model_field='type',
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )

    subcategory = ChainedForeignKey(
        Subcategory,
        chained_field='category',             # зависит от выбранной категории
        chained_model_field='category',
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.PROTECT,
        verbose_name='Подкатегория'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Сумма'
    )

    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )

    class Meta:
        ordering = ['-date']  # Сортировка по дате, от новых к старым

    def __str__(self):
        return f'{self.date.strftime("%d.%m.%Y")} — {self.amount} ₽'
