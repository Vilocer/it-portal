from django.db import models
from django.contrib.auth.models import User
from apps.user.models import Profile

from easy_thumbnails.fields import ThumbnailerImageField
from tinymce import HTMLField
import re
import unidecode

def slugify(text): # function for convert normal text to slug
    text = unidecode.unidecode(text).lower()
    return re.sub(r'[\W_]+', '-', text)

def clean_html(raw_html):
    clean = re.compile('<.*?>')
    cleantext = re.sub(clean, '', raw_html)

    return cleantext

def generate_filename(instance, filename): # generate filename for article image
    filename = 'ArticleImage' + '.' + re.split(r'[.\s]', filename)[-1]
    name = str(instance.pk) + '-' + slugify(instance.title[:20])
    return '{}/{}/{}/{}'.format('articles', instance.category, name, filename)

def generate_filename_for_comment(instance, filename): # generate filename for article image
    filename = 'CommentImage' + '.' + re.split(r'[.\s]', filename)[-1]
    name = str(instance.article.pk) + '-' + slugify(instance.article.title[:20])

    return '{}/{}/{}/{}/{}/{}'.format('articles', instance.article.category, name, 'comments', slugify(str(instance.author)), filename)

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/articles/?category=%s' % self.slug

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    image = ThumbnailerImageField(resize_source={ 'size': (1280, 0), 'crop': 'scale' }, upload_to=generate_filename, verbose_name='Изображение')
    content = HTMLField(verbose_name='Содержание')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    view = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    def content_no_html(self):
        cleaned_content = clean_html(self.content)

        return cleaned_content

    def get_likes_count(self):
        count = len(ArticleLike.objects.filter(article = self))
        return count

    def get_absolute_url(self):
        return '/post/%s' % self.pk

    def __str__(self):
        return(self.title)

    def add_view(self):
        self.view = self.view + 1
        self.save()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-timestamp']

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    content = models.TextField(verbose_name='Содержание', max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    image = ThumbnailerImageField(resize_source={ 'size': (1280, 0), 'crop': 'scale' }, upload_to=generate_filename_for_comment, verbose_name='Картинка к комментарию', blank=True, null=True)

    def __str__(self):
        return (str(self.author))

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class ReplyComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий')
    content = models.TextField(verbose_name='Содержание')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return (str(self.content))

    class Meta:
        verbose_name = 'Ответ к комментарию'
        verbose_name_plural = 'Ответы к комментариям'


class ArticleLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Статья')

    def __str__(self):
        return str(self.profile)

    class Meta:
        verbose_name = 'Отметка нравится'
        verbose_name_plural = 'Отметки нравится'
