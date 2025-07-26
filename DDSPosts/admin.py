"""
Административная панель управления данными.

Регистрирует модели:
- Типы операций
- Категории
- Подкатегории
- Статусы
- Транзакции
"""
from django.contrib import admin
from .models import Status, Type, Category, Subcategory, Transaction


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    """Админка для модели Type (Тип операции)"""
    list_display = ['name']  # Отображать имя в списке


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для модели Category (Категория)"""
    list_display = ['name', 'type']  # Отображать имя и связанный тип
    list_filter = ['type']           # Фильтрация по типу


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Админка для модели Subcategory (Подкатегория)"""
    list_display = ['name', 'category']           # Отображать имя и родительскую категорию
    list_filter = ['category__type']              # Фильтрация по типу через категорию


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Админка для модели Transaction (Транзакция)"""
    list_display = ['formatted_date', 'operation', 'status', 'category', 'subcategory', 'amount']
    list_filter = ['operation', 'status', 'category']
    search_fields = ['comment']  # Поиск по полю "комментарий"

    def formatted_date(self, obj):
        """
        Отображение даты в формате ДД.ММ.ГГГГ вместо стандартного ISO.
        """
        return obj.date.strftime('%d.%m.%Y')

    formatted_date.short_description = 'Дата'  # Заголовок колонки в админке


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Админка для модели Status (Статус операции)"""
    list_display = ['name']
