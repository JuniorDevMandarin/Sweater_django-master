from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from ckeditor.fields import RichTextField


class Social(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    # content = models.TextField(blank=True, verbose_name='Текст статьи')
    content = RichTextField(blank=True, verbose_name='Текст статьи')
    body = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Post'
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="photos/%Y/%m/%d/", default="<path>/default_profile_pic.png")
    website_url = models.CharField(max_length=255, null=True, blank=True, )
    facebook_url = models.CharField(max_length=255, null=True, blank=True, )
    github_url = models.CharField(max_length=255, null=True, blank=True, )
    insta_url = models.CharField(max_length=255, null=True, blank=True, )

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('home')


class Comment(models.Model):
    post = models.ForeignKey(Social, related_name='comments', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)