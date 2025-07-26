"""
URL-маршруты.

Включает:
- Основные страницы (главная, создание, редактирование, удаление транзакции)
- AJAX-запросы для динамической подгрузки категорий/подкатегорий
- Панель управления справочниками и действия с ними
"""

from django.urls import path
from .views import (
    # Транзакции
    TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView,
    # AJAX-подгрузка
    load_categories, load_subcategories,
    # Справочники
    directory_panel,
    StatusCreateView, StatusUpdateView, StatusDeleteView,
    TypeCreateView, TypeUpdateView, TypeDeleteView,
    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    SubcategoryCreateView, SubcategoryUpdateView, SubcategoryDeleteView
)

# Основные страницы: список, создание, редактирование, удаление транзакции
urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction_list'),  # Главная страница со списком транзакций
    path('create/', TransactionCreateView.as_view(), name='create'),   # Страница создания транзакции
    path('edit/<int:pk>/', TransactionUpdateView.as_view(), name='edit'),  # Страница редактирования транзакции
    path('delete/<int:pk>/', TransactionDeleteView.as_view(), name='delete'),  # Страница удаления транзакции
]

# AJAX-запросы для динамического обновления категорий и подкатегорий
urlpatterns += [
    path('ajax/load-categories/', load_categories, name='ajax_load_categories'),
    path('ajax/load-subcategories/', load_subcategories, name='ajax_load_subcategories'),
]

# Панель управления справочниками и действия с ними
urlpatterns += [
    path('directories/', directory_panel, name='directory_panel'),

    # CRUD для Статусов
    path('directories/status/add/', StatusCreateView.as_view(), name='status_add'),
    path('directories/status/<int:pk>/edit/', StatusUpdateView.as_view(), name='status_edit'),
    path('directories/status/<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),

    # CRUD для Типов
    path('directories/type/add/', TypeCreateView.as_view(), name='type_add'),
    path('directories/type/<int:pk>/edit/', TypeUpdateView.as_view(), name='type_edit'),
    path('directories/type/<int:pk>/delete/', TypeDeleteView.as_view(), name='type_delete'),

    # CRUD для Категорий
    path('directories/category/add/', CategoryCreateView.as_view(), name='category_add'),
    path('directories/category/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('directories/category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # CRUD для Подкатегорий
    path('directories/subcategory/add/', SubcategoryCreateView.as_view(), name='subcategory_add'),
    path('directories/subcategory/<int:pk>/edit/', SubcategoryUpdateView.as_view(), name='subcategory_edit'),
    path('directories/subcategory/<int:pk>/delete/', SubcategoryDeleteView.as_view(), name='subcategory_delete'),
]
