from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField()

	def __str__(self):
		return self.name

class Article(models.Model):
	PAGE_TYPES = (
		(1, 'post'),
		(2, 'page'),
	)
	title = models.CharField(max_length=255)
	excerpt = models.TextField()
	content = models.TextField()
	slug = models.SlugField()
	thumbnail = models.ImageField()
	layout = models.SmallIntegerField(choices=PAGE_TYPES, default=1)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class Publication(models.Model):
	title = models.CharField(max_length=255)
	slug = models.SlugField()
	abstract = models.TextField()
	authors = models.CharField(max_length=255)
	journal = models.CharField(max_length=100)
	year = models.SmallIntegerField()
	volume = models.CharField(max_length=10)
	issue = models.CharField(max_length=10)
	pages = models.CharField(max_length=20)
	doi = models.CharField(max_length=100)
	factor = models.FloatField()
	thumbnail = models.ImageField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

class Member(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField()
	title = models.CharField(max_length=30)
	email = models.EmailField()
	degree = models.CharField(max_length=30)
	experience = models.TextField()

	def __str__(self):
		return self.name

class Slideshow(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField()
	image = models.ImageField()
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


@receiver(pre_delete, sender=Slideshow)
def delete_image(sender, instance, **kwargs):
	instance.image.delete(False)

@receiver(pre_delete, sender=Article)
def delete_thumbnail(sender, instance, **kwargs):
	instance.thumbnail.delete(False)

@receiver(pre_delete, sender=Publication)
def delete_publication(sender, instance, **kwargs):
	instance.thumbnail.delete(False)
