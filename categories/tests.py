from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from main.models import Product
from django.shortcuts import reverse
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


    def test_categories_url_is_exist(self):
        self.setCustomer()
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)

    def test_admin_categories_template(self):
        self.setAdmin()
        response = self.client.get('/admin-categories/')
        self.assertTemplateUsed(response, 'categories_admin.html')

    @csrf_exempt
    def test_add_product_ajax_cat(self):
        self.setAdmin()
        url = '/add-product-ajax-cat/'
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            "name": "Food",
            "price": 50000,
            "restaurant": "New Restaurant",
            "location": "Somewhere in Bandung",
            "contact": "9876543210",
            "cat": "Makanan Berat dan Nasi",
            "image": image,
        }

        response = self.client.post(url, data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name="Food").exists())
