from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal

from .models import Type, Category, Subcategory, Status, Transaction
from .forms import TransactionForm

class TransactionModelTest(TestCase):
    """Тестирование модели Transaction"""
    def setUp(self):
        # Подготовка начальных данных
        self.status = Status.objects.create(name="Бизнес")
        self.operation_type = Type.objects.create(name="Списание")
        self.category = Category.objects.create(name="Маркетинг", type=self.operation_type)
        self.subcategory = Subcategory.objects.create(name="Avito", category=self.category)

    def test_transaction_creation(self):
        """Проверка создания транзакции"""
        transaction = Transaction.objects.create(
            date=timezone.now(),
            status=self.status,
            operation=self.operation_type,
            category=self.category,
            subcategory=self.subcategory,
            amount=Decimal("1000.50"),
            comment="Тестовая транзакция"
        )
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(transaction.comment, "Тестовая транзакция")
        self.assertEqual(transaction.status.name, "Бизнес")

class ViewTests(TestCase):
    """Тесты представлений"""
    def setUp(self):
        self.status = Status.objects.create(name="Личное")
        self.type = Type.objects.create(name="Пополнение")
        self.category = Category.objects.create(name="Зарплата", type=self.type)
        self.subcategory = Subcategory.objects.create(name="Бонус", category=self.category)

        self.transaction = Transaction.objects.create(
            date=timezone.now(),
            status=self.status,
            operation=self.type,
            category=self.category,
            subcategory=self.subcategory,
            amount=Decimal("5000"),
            comment="Тестовый доход"
        )

    def test_transaction_list_view(self):
        """Главная страница отображает список транзакций"""
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовый доход")

    def test_transaction_create_view_get(self):
        """Форма создания отображается корректно"""
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тип операции")

    def test_transaction_delete_view(self):
        """Удаление транзакции"""
        response = self.client.post(reverse('delete', args=[self.transaction.id]))
        self.assertRedirects(response, reverse('transaction_list'))
        self.assertEqual(Transaction.objects.count(), 0)


class TransactionFormTest(TestCase):
    """Тест формы TransactionForm"""
    def setUp(self):
        self.status = Status.objects.create(name="Налог")
        self.type = Type.objects.create(name="Списание")
        self.category = Category.objects.create(name="Реклама", type=self.type)
        self.subcategory = Subcategory.objects.create(name="Google Ads", category=self.category)

    def test_valid_form(self):
        """Форма валидна при корректных данных"""
        form_data = {
            'date': timezone.now(),
            'status': self.status.id,
            'operation': self.type.id,
            'category': self.category.id,
            'subcategory': self.subcategory.id,
            'amount': '1234.56',
            'comment': 'Проверка формы'
        }
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        """Форма невалидна при отсутствии обязательных полей"""
        form_data = {
            'comment': 'Неполная форма'
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors)
        self.assertIn('operation', form.errors)
        self.assertIn('amount', form.errors)

class AjaxDropdownTest(TestCase):
    """Тесты AJAX. Загрузки категорий и подкатегорий"""
    def setUp(self):
        self.type = Type.objects.create(name="Пополнение")
        self.category = Category.objects.create(name="Зарплата", type=self.type)
        self.subcategory = Subcategory.objects.create(name="Бонус", category=self.category)

    def test_load_categories_view(self):
        """Загрузка категорий по выбранному типу"""
        response = self.client.get(reverse('ajax_load_categories'), {'type_id': self.type.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_load_subcategories_view(self):
        """Загрузка подкатегорий по выбранной категории"""
        response = self.client.get(reverse('ajax_load_subcategories'), {'category_id': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.subcategory.name)
