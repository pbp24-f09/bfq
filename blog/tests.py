from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import CustomUser
from .models import Article

class ArticleModelTest(TestCase):
    
    def setUp(self):
        # Buat user dengan CustomUser untuk testing
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='12345',
            age=20  # Tambahkan age atau nilai default lainnya
        )
        # Buat instance Article untuk testing
        self.article = Article.objects.create(
            title='Judul Test',
            topic='Kuliner',
            content='Ini adalah konten artikel.',
            author=self.user
        )

    def test_article_creation(self):
        # Pastikan artikel dibuat dengan benar
        self.assertEqual(self.article.title, 'Judul Test')
        self.assertEqual(self.article.topic, 'Kuliner')
        self.assertEqual(self.article.content, 'Ini adalah konten artikel.')
        self.assertEqual(self.article.author, self.user)
    
    def test_string_representation(self):
        # Cek representasi string dari model
        self.assertEqual(str(self.article), 'Judul Test')


class ArticleViewsTest(TestCase):

    def setUp(self):
        # Setup CustomUser dan client untuk testing
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='12345',
            age=20  # Tambahkan age atau nilai default lainnya
        )
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        self.url_create_article = reverse('blog:create_article_ajax')

    def test_create_article_ajax(self):
        # Test pembuatan artikel menggunakan AJAX
        response = self.client.post(self.url_create_article, {
            'title': 'Artikel Baru',
            'topic': 'Edukasi',
            'content': 'Konten artikel baru'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Article.objects.filter(title='Artikel Baru').exists())

        response_json = response.json()
        # Cek hanya bagian 'success' dari response
        self.assertEqual(response_json.get('success'), True)


    def test_article_list(self):
        # Test tampilan daftar artikel
        response = self.client.get(reverse('blog:article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_list.html')

    def test_delete_article(self):
        # Test penghapusan artikel
        article = Article.objects.create(
            title='Judul Hapus',
            topic='Sosial',
            content='Konten yang akan dihapus',
            author=self.user
        )

        response = self.client.post(reverse('blog:delete_article', args=[article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Article.objects.filter(pk=article.id).exists())
