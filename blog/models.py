from django.db import models
from django.conf import settings  # Tambahkan import ini

class Article(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Otomatis diisi saat dibuat
    updated_at = models.DateTimeField(auto_now=True)      # Otomatis diisi saat diperbarui

    def __str__(self):
        return self.title
