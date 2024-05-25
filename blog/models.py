from django.db import models
from PIL import Image

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    overview = models.TextField(max_length=350, verbose_name='содержимое', **NULLABLE)
    preview = models.ImageField(default='placeholder.png', upload_to='', verbose_name='изображение', **NULLABLE)
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    view_counter = models.IntegerField(default=0, verbose_name='кол-во просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.preview:
            image = Image.open(self.preview.path)
            target_size = (300, 300)
            image.thumbnail(target_size)
            image.save(self.preview.path)
