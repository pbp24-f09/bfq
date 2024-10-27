from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from main.models import Product
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from authentication.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.views.decorators.csrf import csrf_exempt

class categoriesTest(TestCase):
    def setCustomer(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser1',
            password='testpw_312',
            full_name='Test User Customer',
            email='testuser1@example.com',
            age=30,
            gender='MALE',
            phone_number='1234567890',
            role='customer',
        )
        self.client.login(username='testuser1', password='testpw_312')

    def setAdmin(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser2',
            password='testpw_456',
            full_name='Test User Admin',
            email='testuser2@example.com',
            age=28,
            gender='MALE',
            phone_number='08123456789',
            role='admin',
        )
        self.client.login(username='testuser2', password='testpw_456')

        self.product = Product.objects.create(
            name='Food',
            price=50000,
            restaurant='Test Restaurant',
            location='Somewhere in Bandung',
            contact='08123456789',
            cat='Makanan Berat dan Nasi',
            user=self.user
        )

    # Check if the URL is valid
    def test_categories_url_is_exist(self):
        self.setCustomer()
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)

    # Check if the admin's categories template is rendered
    def test_admin_categories_template(self):
        self.setAdmin()
        response = self.client.get('/admin-categories/')
        self.assertTemplateUsed(response, 'categories_admin.html')

    # Check if a product can be deleted successfully
    def test_delete_product_cat(self):
        self.setAdmin()
        url = reverse('categories:delete_product_cat', args=[self.product.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
