"""
Представления приложения.

Содержит:
- Представления CRUD для справочников: Статус, Тип, Категория, Подкатегория
- Представления для транзакций (создание, редактирование, удаление, список)
- Панель управления справочниками
- AJAX-загрузку зависимых категорий и подкатегорий
"""

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Transaction, Type, Status, Category, Subcategory
from .forms import TransactionForm, StatusForm, TypeForm, CategoryForm, SubcategoryForm


# ---------- СПРАВОЧНИКИ ----------

class StatusCreateView(CreateView):
    """Создание статуса"""
    model = Status
    form_class = StatusForm
    template_name = 'DDSPosts/status_form.html'
    success_url = reverse_lazy('directory_panel')


class StatusUpdateView(UpdateView):
    """Редактирование статуса"""
    model = Status
    form_class = StatusForm
    template_name = 'DDSPosts/status_form.html'
    success_url = reverse_lazy('directory_panel')


class StatusDeleteView(DeleteView):
    """Удаление статуса"""
    model = Status
    template_name = 'DDSPosts/status_confirm_delete.html'
    success_url = reverse_lazy('directory_panel')


class TypeCreateView(CreateView):
    """Создание типа операции"""
    model = Type
    form_class = TypeForm
    template_name = 'DDSPosts/type_form.html'
    success_url = reverse_lazy('directory_panel')


class TypeUpdateView(UpdateView):
    """Редактирование типа операции"""
    model = Type
    form_class = TypeForm
    template_name = 'DDSPosts/type_form.html'
    success_url = reverse_lazy('directory_panel')


class TypeDeleteView(DeleteView):
    """Удаление типа операции"""
    model = Type
    template_name = 'DDSPosts/type_confirm_delete.html'
    success_url = reverse_lazy('directory_panel')


class CategoryCreateView(CreateView):
    """Создание категории"""
    model = Category
    form_class = CategoryForm
    template_name = 'DDSPosts/category_form.html'
    success_url = reverse_lazy('directory_panel')


class CategoryUpdateView(UpdateView):
    """Редактирование категории"""
    model = Category
    form_class = CategoryForm
    template_name = 'DDSPosts/category_form.html'
    success_url = reverse_lazy('directory_panel')


class CategoryDeleteView(DeleteView):
    """Удаление категории"""
    model = Category
    template_name = 'DDSPosts/category_confirm_delete.html'
    success_url = reverse_lazy('directory_panel')


class SubcategoryCreateView(CreateView):
    """Создание подкатегории"""
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'DDSPosts/subcategory_form.html'
    success_url = reverse_lazy('directory_panel')


class SubcategoryUpdateView(UpdateView):
    """Редактирование подкатегории"""
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'DDSPosts/subcategory_form.html'
    success_url = reverse_lazy('directory_panel')


class SubcategoryDeleteView(DeleteView):
    """Удаление подкатегории"""
    model = Subcategory
    template_name = 'DDSPosts/subcategory_confirm_delete.html'
    success_url = reverse_lazy('directory_panel')


def directory_panel(request):
    """
    Панель управления справочниками:
    отображает все статусы, типы, категории и подкатегории.
    """
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.select_related('type')
    subcategories = Subcategory.objects.select_related('category')

    return render(request, 'DDSPosts/directory_panel.html', {
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
    })


# ---------- ТРАНЗАКЦИИ ----------

class TransactionCreateView(CreateView):
    """Создание новой транзакции"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'DDSPosts/create.html'
    success_url = reverse_lazy('transaction_list')


class TransactionUpdateView(UpdateView):
    """Редактирование транзакции"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'DDSPosts/create.html'
    success_url = reverse_lazy('transaction_list')


class TransactionDeleteView(DeleteView):
    """Удаление транзакции"""
    model = Transaction
    template_name = 'DDSPosts/delete_confirm.html'
    success_url = reverse_lazy('transaction_list')


class TransactionListView(ListView):
    """Главная страница: список транзакций с фильтрацией"""
    model = Transaction
    template_name = 'base.html'
    context_object_name = 'transactions'
    paginate_by = 25

    def get_queryset(self):
        """Фильтрация по параметрам из формы"""
        qs = super().get_queryset()
        filters = self.request.GET

        if filters.get('date'):
            qs = qs.filter(date=filters['date'])

        if filters.get('status'):
            qs = qs.filter(status__id=filters['status'])

        if filters.get('type'):
            qs = qs.filter(operation__id=filters['type'])

        if filters.get('category'):
            qs = qs.filter(category__id=filters['category'])

        if filters.get('subcategory'):
            qs = qs.filter(subcategory__id=filters['subcategory'])

        return qs

    def get_context_data(self, **kwargs):
        """Добавляет фильтры и справочники в контекст шаблона"""
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all()
        context['statuses'] = Status.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['filters'] = self.request.GET
        return context


# ---------- AJAX каскадная фильтрация ----------

def load_categories(request):
    """
    AJAX: возвращает категории, связанные с выбранным типом
    """
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).order_by('name')
    return render(request, 'DDSPosts/dropdown_category.html', {'categories': categories})


def load_subcategories(request):
    """
    AJAX: возвращает подкатегории, связанные с выбранной категорией
    """
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'DDSPosts/dropdown_subcategory.html', {'subcategories': subcategories})
