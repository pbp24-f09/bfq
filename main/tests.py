from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Product
from main.forms import ProductForm
from django.utils import timezone
import json

class MainViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.product = Product.objects.create(
            name="Test Product",
            price=100,
            restaurant="Test Restaurant",
            location="Test Location",
            contact="123456789",
            cat="Test Category",
            user=self.user
        )

    def test_show_main_view(self):
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main.html")
        self.assertIn('Bandung Nice Food', response.context['tagline'])

    def test_show_main_admin_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('main:show_main_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main_admin.html")
        self.assertIn('Bandung Nice Food', response.context['tagline'])

    def test_create_product_view_post(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('main:create_product'), {
            'name': 'New Product',
            'price': 200,
            'restaurant': 'New Restaurant',
            'location': 'New Location',
            'contact': '987654321',
            'cat': 'New Category',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 2)

    def test_show_xml_view(self):
        response = self.client.get(reverse('main:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_view(self):
        response = self.client.get(reverse('main:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)

    def test_show_xml_by_id_view(self):
        response = self.client.get(reverse('main:show_xml_by_id', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

    def test_show_json_by_id_view(self):
        response = self.client.get(reverse('main:show_json_by_id', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(data[0]['pk'], self.product.id)

    def test_edit_product_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('main:edit_product', args=[self.product.id]), {
            'name': 'Updated Product',
            'price': 150,
            'restaurant': 'Updated Restaurant',
            'location': 'Updated Location',
            'contact': '555555555',
            'cat': 'Updated Category',
        })
        self.assertEqual(response.status_code, 302)
        updated_product = Product.objects.get(pk=self.product.id)
        self.assertEqual(updated_product.name, 'Updated Product')

    def test_delete_product_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('main:delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=self.product.id).exists())

    def test_add_product_ajax_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('main:add_product_ajax'), {
            'name': 'Ajax Product',
            'price': 300,
            'restaurant': 'Ajax Restaurant',
            'location': 'Ajax Location',
            'contact': '333333333',
            'cat': 'Ajax Category',
            'image': None,
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name="Ajax Product").exists())
