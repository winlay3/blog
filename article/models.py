from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
# Create your models here.
class Author(AbstractUser):
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name

class Article(models.Model):
    image = models.ImageField(upload_to="blog/")
    title = models.CharField(max_length=60)
    #content
    content = RichTextField()
    is_publish = models.BooleanField(default=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name="article")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="article")
    def __str__(self):
        return f'{self.title} (Author - {self.author})'
