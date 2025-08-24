from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import messages

from basket.models import CartAndUser, CartAndProduct
from products.models import Product, Category
from users.models import User


class CartTest(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.category = Category.objects.create(
            name='test category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            category=self.category,
            quantity=10
        )

    def test_add_to_cart_authenticated_user(self):
        """Тест добавления товара в корзину аутентифицированным пользователем"""
        self.client.login(username='testuser', password='testpass123')
        self.assertFalse(CartAndUser.objects.filter(user_id=self.user.id).exists())

        response = self.client.post(
            reverse('cart:add_to_cart', kwargs={'product_id': self.product.id})
        )

        # Проверяем редирект
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))

        # Проверяем, что корзина создана
        cart_user = CartAndUser.objects.get(user_id=self.user.id)

        # Проверяем, что товар добавлен в корзину
        cart_product = CartAndProduct.objects.get(
            cart=cart_user,
            product=self.product
        )
        self.assertEqual(cart_product.quantity, 1)

    def test_add_to_cart_unauthenticated_user(self):
        """Тест добавления товара неаутентифицированным пользователем"""
        response = self.client.post(
            reverse('cart:add_to_cart', kwargs={'product_id': self.product.id})
        )

        # Проверяем редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

    def test_add_to_cart_existing_product(self):
        """Тест увеличения количества существующего товара"""
        self.client.login(username='testuser', password='testpass123')

        # Сначала вызываем представление, чтобы создать корзину
        self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}))

        # Добавляем тот же товар еще раз
        response = self.client.post(
            reverse('cart:add_to_cart', kwargs={'product_id': self.product.id})
        )

        # Проверяем, что количество увеличилось
        cart_user = CartAndUser.objects.get(user_id=self.user.id)
        cart_product = CartAndProduct.objects.get(
            cart=cart_user,
            product=self.product
        )
        self.assertEqual(cart_product.quantity, 2)

    def test_add_to_cart_exceeds_stock(self):
        """Тест добавления товара, превышающего количество на складе"""
        self.client.login(username='testuser', password='testpass123')

        # Устанавливаем маленькое количество на складе
        self.product.quantity = 1
        self.product.save()

        # Создаем корзину через представление
        self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}))

        # Пытаемся добавить еще одну (должно превысить лимит)
        response = self.client.post(
            reverse('cart:add_to_cart', kwargs={'product_id': self.product.id})
        )

        # Проверяем, что количество не изменилось
        cart_user = CartAndUser.objects.get(user_id=self.user.id)
        cart_product = CartAndProduct.objects.get(
            cart=cart_user,
            product=self.product
        )
        self.assertEqual(cart_product.quantity, 1)

    def test_cart_remove_authenticated_user(self):
        """Тест удаления товара из корзины"""
        self.client.login(username='testuser', password='testpass123')

        # Сначала добавляем товар через представление
        self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}))

        response = self.client.post(
            reverse('cart:remove_from_cart', kwargs={'product_id': self.product.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))

        # Проверяем, что товар удален
        cart_user = CartAndUser.objects.get(user_id=self.user.id)
        cart_product = CartAndProduct.objects.filter(
            cart=cart_user,
            product=self.product
        ).first()
        self.assertIsNone(cart_product)

    def test_cart_remove_unauthenticated_user(self):
        """Тест удаления товара неаутентифицированным пользователем"""
        response = self.client.post(
            reverse('cart:remove_from_cart', kwargs={'product_id': self.product.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

    def test_delete_item_authenticated_user(self):
        """Тест уменьшения количества товара"""
        self.client.login(username='testuser', password='testpass123')

        # Добавляем товар два раза (количество = 2)
        self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}))
        self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}))

        # Уменьшаем количество
        response = self.client.post(
            reverse('cart:delete_item', kwargs={'product_id': self.product.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))

        # Проверяем, что количество уменьшилось до 1
        cart_user = CartAndUser.objects.get(user_id=self.user.id)
        cart_product = CartAndProduct.objects.get(
            cart=cart_user,
            product=self.product
        )
        self.assertEqual(cart_product.quantity, 1)

    def test_delete_item_last_item(self):
        """Тест удаления последнего товара"""
        self.client.login(username='testuser', password='testpass123')

        # Добавляем товар
        self.client.post(reverse('cart:add_to_cart', kwargs={'product_id': self.product.id}))

        # Удаляем последний товар
        response = self.client.post(
            reverse('cart:delete_item', kwargs={'product_id': self.product.id})
        )

        # Проверяем, что товар удален
        cart_user = CartAndUser.objects.get(user_id=self.user.id)
        cart_product = CartAndProduct.objects.filter(
            cart=cart_user,
            product=self.product
        ).first()
        self.assertIsNone(cart_product)

    def test_cart_detail_authenticated_user(self):
        """Тест просмотра корзины аутентифицированным пользователем"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('cart:cart_detail'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/cart.html')
        self.assertIn('cart', response.context)
        self.assertIn('price', response.context)

    def test_cart_detail_unauthenticated_user(self):
        """Тест просмотра корзины неаутентифицированным пользователем"""
        response = self.client.get(reverse('cart:cart_detail'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

    def test_cart_detail_empty_cart(self):
        """Тест просмотра пустой корзины"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('cart:cart_detail'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cart']), 0)
        self.assertEqual(response.context['price'], 0)