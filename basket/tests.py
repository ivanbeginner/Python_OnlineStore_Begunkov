from django.test import TestCase,Client
from django.urls import reverse

from basket.models import CartAndUser, CartAndProduct
from products.models import Product, Category
from users.models import User


# Create your tests here.
class CartTest(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category=Category.objects.create(
            name='test category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            category=self.category
        )
        self.cart = CartAndUser.objects.create(user=self.user)
    def test_add_to_cart_authenticated_user(self):
        """Тест добавления товара в корзину аутентифицированным пользователем"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(
            reverse('cart:add_to_cart', kwargs={'product_id': self.product.id})
        )

        # Проверяем редирект
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))

        # Проверяем, что товар добавлен в корзину
        cart_product = CartAndProduct.objects.filter(
            cart=self.cart,
            product=self.product
        ).first()
        self.assertIsNotNone(cart_product)
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

        # Сначала добавляем товар
        CartAndProduct.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )

        # Добавляем тот же товар еще раз
        response = self.client.post(
            reverse('cart:add_to_cart', kwargs={'product_id': self.product.id})
        )

        # Проверяем, что количество увеличилось
        cart_product = CartAndProduct.objects.get(
            cart=self.cart,
            product=self.product
        )
        self.assertEqual(cart_product.quantity, 2)

    def test_cart_remove_authenticated_user(self):
        """Тест удаления товара из корзины"""
        self.client.login(username='testuser', password='testpass123')

        # Сначала добавляем товар
        CartAndProduct.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )

        response = self.client.post(
            reverse('cart:remove_from_cart', kwargs={'product_id': self.product.id})
        )


        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))


        cart_product = CartAndProduct.objects.filter(
            cart=self.cart,
            product=self.product
        ).first()
        self.assertIsNone(cart_product)

    def test_cart_remove_unauthenticated_user(self):
        """Тест удаления товара неаутентифицированным пользователем"""
        response = self.client.post(
            reverse('cart:remove_from_cart', kwargs={'product_id': self.product.id})
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_item_authenticated_user(self):
        """Тест уменьшения количества товара"""
        self.client.login(username='testuser', password='testpass123')
        # Создаем товар с количеством 2
        CartAndProduct.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )

        response = self.client.post(
            reverse('cart:delete_item', kwargs={'product_id': self.product.id})
        )


        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))
        cart_product = CartAndProduct.objects.get(
            cart=self.cart,
            product=self.product
        )
        self.assertEqual(cart_product.quantity, 1)

    def test_delete_item_last_item(self):
        """Тест удаления последнего товара"""
        self.client.login(username='testuser', password='testpass123')

        # Создаем товар с количеством 1
        CartAndProduct.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )

        response = self.client.post(
            reverse('cart:delete_item', kwargs={'product_id': self.product.id})
        )


        cart_product = CartAndProduct.objects.filter(
            cart=self.cart,
            product=self.product
        ).first()
        self.assertEqual(cart_product,None)
