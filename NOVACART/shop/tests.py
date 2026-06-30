from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Order, OrderItem, Product


class StorefrontTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_cart_page_loads(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)


class OrderHistoryTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='buyer', password='pass1234')
        self.staff = get_user_model().objects.create_user(username='admin', password='pass1234', is_staff=True, is_superuser=True)

    def test_user_can_view_their_own_orders(self):
        product = Product.objects.create(name='Test Lamp', description='Nice lamp', price=Decimal('25.00'), stock=3)
        order = Order.objects.create(
            user=self.user,
            customer_name='Buyer One',
            address='123 Main',
            city='London',
            zip_code='SW1A',
            phone='123456789',
            total=Decimal('25.00'),
        )
        OrderItem.objects.create(order=order, product=product, quantity=1, price=product.price)

        self.client.force_login(self.user)
        response = self.client.get(reverse('my_orders'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buyer One')

    def test_staff_can_view_all_orders(self):
        other_user = get_user_model().objects.create_user(username='other', password='pass1234')
        product = Product.objects.create(name='Test Mouse', description='Wireless mouse', price=Decimal('15.00'), stock=4)
        order = Order.objects.create(
            user=other_user,
            customer_name='Other Customer',
            address='10 Side',
            city='Paris',
            zip_code='75000',
            phone='987654321',
            total=Decimal('15.00'),
        )
        OrderItem.objects.create(order=order, product=product, quantity=1, price=product.price)

        self.client.force_login(self.staff)
        response = self.client.get(reverse('admin_orders'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Other Customer')

    def test_logout_redirects_to_home(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))

        self.assertRedirects(response, reverse('home'))

    def test_homepage_keeps_authenticated_session(self):
        self.client.force_login(self.user)
        self.client.get(reverse('home'))

        self.assertEqual(self.client.session['_auth_user_id'], str(self.user.pk))
