from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField()

	def __str__(self):
		return self.name

class Article(models.Model):
	PAGE_TYPE = (
		(1, 'post'),
		(2, 'page'),
	)
	title = models.CharField(max_length=255)
	excerpt = models.TextField()
	content = models.TextField()
	slug = models.SlugField()
	layout = models.SmallIntegerField(choices=PAGE_TYPE, default=1)
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
	volume = models.CharField(max_length=10)
	issue = models.CharField(max_length=10)
	pages = models.CharField(max_length=20)
	doi = models.CharField(max_length=100)
	factor = models.FloatField()
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

