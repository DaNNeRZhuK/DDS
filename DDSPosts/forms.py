"""
Формы для приложения.

Содержит формы для:
- Транзакции
- Типа операции
- Категории
- Подкатегории
- Статуса

Формы используют Bootstrap-классы и поддерживают каскадную фильтрацию.
"""

from django import forms
from .models import Transaction, Category, Subcategory, Status, Type


class SubcategoryForm(forms.ModelForm):
    """Форма для создания и редактирования подкатегории"""
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


class CategoryForm(forms.ModelForm):
    """Форма для создания и редактирования категории"""
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }


class TypeForm(forms.ModelForm):
    """Форма для создания и редактирования типа операции"""
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StatusForm(forms.ModelForm):
    """Форма для создания и редактирования статуса"""
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TransactionForm(forms.ModelForm):
    """
    Форма для создания и редактирования транзакции.
    Реализует каскадную фильтрацию: тип -> категория -> подкатегория.
    """
    class Meta:
        model = Transaction
        fields = ['date', 'operation', 'category', 'subcategory', 'status', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы с каскадной логикой фильтрации полей"""
        super().__init__(*args, **kwargs)

        # Применение Bootstrap-стилей к select-полям
        for field in self.fields:
            if field not in ['comment', 'date', 'amount']:
                self.fields[field].widget.attrs['class'] = 'form-select'

        # Изначально скрываем категории и подкатегории
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        # Если в POST-запросе передан выбранный тип
        if 'operation' in self.data:
            try:
                operation_id = int(self.data.get('operation'))
                self.fields['category'].queryset = Category.objects.filter(type_id=operation_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Если редактируем существующую транзакцию
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.operation)

        # Если в POST-запросе передана выбранная категория
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
