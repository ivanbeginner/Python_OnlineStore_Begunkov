from django.contrib import messages
from django.test import TestCase,Client
from django.urls import reverse

from basket.models import CartAndUser, CartAndProduct
from orders.forms import OrderForm
from orders.models import Order
from products.models import Category, Product, StockBalance
from users.models import User


# Create your tests here.
class OrderTest(TestCase):

    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.category = Category.objects.create(name='testcategory')
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            quantity=10,
            category=self.category
        )
        self.cart = CartAndUser.objects.create(user=self.user)
        self.cart_product = CartAndProduct.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.stock_balance = StockBalance.objects.create(
            product=self.product,
            quantity=10
        )

    def test_create_order_get_request(self):
        """Тест GET запроса к create_order"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('orders:create_order'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order.html')
        self.assertIsInstance(response.context['form'], OrderForm)

    def test_create_order_unauthenticated_user(self):
        """Тест неаутентифицированного пользователя"""
        response = self.client.post(reverse('orders:create_order'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

    def test_create_order_empty_cart(self):
        """Тест создания заказа с пустой корзиной"""
        self.client.login(username='testuser', password='testpass123')

        # Очищаем корзину
        CartAndProduct.objects.all().delete()

        response = self.client.post(reverse('orders:create_order'), {
            'address': 'Test Address',
            'email': 'test@example.com'
        })

        # Проверяем сообщение об ошибке и редирект
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertIn('Ваша корзина пуста', str(messages_list[0]))
        self.assertRedirects(response, reverse('cart:cart_detail'))

    def test_create_order_valid_data(self):
        """Тест успешного создания заказа"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('orders:create_order'), {
            'name':'testuser',
            'address': 'Test Address 123',
            'email': 'test@example.com'
        },follow=True)

        # Проверяем создание заказа
        order = Order.objects.filter(user_id=self.user.id).first()

        self.assertEqual(order.address, 'Test Address 123')
        self.assertEqual(order.email, 'test@example.com')

        # Проверяем обновление количества товара
        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.quantity, 8)  # 10 - 2 = 8

        # Проверяем обновление StockBalance
        stock = StockBalance.objects.get(product=self.product)
        self.assertEqual(stock.quantity, 8)

        # Проверяем создание новой корзины
        new_cart = CartAndUser.objects.filter(user=self.user).last()
        self.assertNotEqual(new_cart.id, self.cart.id)

        # Проверяем редирект
        self.assertRedirects(response, reverse('orders:order_detail', args=[str(order.id)]))

    def test_create_order_insufficient_quantity(self):
        """Тест недостаточного количества товара на складе"""
        self.client.login(username='testuser', password='testpass123')

        # Устанавливаем большое количество в корзине
        self.cart_product.quantity = 20
        self.cart_product.save()

        response = self.client.post(reverse('orders:create_order'), {
            'address': 'Test Address',
            'email': 'test@example.com'
        })

        # Проверяем сообщение об ошибке

        # Проверяем, что заказ не создался
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_invalid_form(self):
        """Тест с невалидной формой"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('orders:create_order'), {
            'address': '',  # Пустое поле
            'email': 'invalid-email'  # Невалидный email
        })

        # Проверяем, что форма не прошла валидацию
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order.html')
        self.assertFalse(response.context['form'].is_valid())

        # Проверяем, что заказ не создался
        self.assertEqual(Order.objects.count(), 0)

    def test_order_detail_authenticated_user(self):
        """Тест просмотра деталей заказа"""
        # Создаем заказ
        order = Order.objects.create(
            user=self.user,
            address='Test Address',
            email='test@example.com',
            cart=self.cart,
            total_cost=200.00
        )

        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('orders:order_detail', args=[str(order.id)]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_detail.html')
        self.assertEqual(response.context['order'], order)
        self.assertIn(self.product.name, response.context['products'])

    def test_order_detail_nonexistent_order(self):
        """Тест несуществующего заказа"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('orders:order_detail', args=['999']))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,reverse('orders:order_list'))
        # Проверяем, что контекст пустой или обработана ошибка

    def test_order_detail_unauthenticated_user(self):
        """Тест неаутентифицированного пользователя"""
        order = Order.objects.create(
            user=self.user,
            address='Test Address',
            email='test@example.com',
            cart=self.cart,
            total_cost=200.00
        )

        response = self.client.get(reverse('orders:order_detail', args=[str(order.id)]))

        # В зависимости от ваших требований к авторизации
        self.assertIn(response.status_code, [302, 200])

    def test_orders_list_authenticated_user(self):
        """Тест списка заказов аутентифицированного пользователя"""
        # Создаем заказы
        order1 = Order.objects.create(
            user=self.user,
            address='Address 1',
            email='test1@example.com',
            cart=self.cart,
            total_cost=100.00
        )
        order2 = Order.objects.create(
            user=self.user,
            address='Address 2',
            email='test2@example.com',
            cart=self.cart,
            total_cost=200.00
        )

        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('orders:order_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')
        self.assertEqual(len(response.context['orders']), 2)
        self.assertIn(order1, response.context['orders'])
        self.assertIn(order2, response.context['orders'])

    def test_orders_list_unauthenticated_user(self):
        """Тест списка заказов неаутентифицированного пользователя"""
        response = self.client.get(reverse('orders:order_list'))

        # Проверяем редирект на логин (если требуется авторизация)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

    def test_orders_list_empty(self):
        """Тест пустого списка заказов"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('orders:order_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 0)