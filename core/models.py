from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
	author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Автор', blank = True, null = True) # blank and null tells that it's not required info
	created_date = models.DateTimeField(auto_now = True)
	name = models.CharField(max_length = 200, verbose_name = 'Название')
	text = models.TextField(verbose_name = 'Текст')

	def __str__(self):
		return '%s: %s' % (self.name, self.created_date)

	class Meta:
		verbose_name = 'статью'
		verbose_name_plural = 'Статьи'

class Comment(models.Model):
	article = models.ForeignKey(Article, on_delete = models.CASCADE, verbose_name = 'Статья', blank = True, null = True, related_name = 'comments_article')
	author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Автор', blank = True, null = True)
	created_date = models.DateTimeField(auto_now = True)
	text = models.TextField(verbose_name = 'Текст')
	status = models.BooleanField(verbose_name = 'Видимость', default = False)