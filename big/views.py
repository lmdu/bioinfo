from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
	posts = Article.objects.filter(layout=1)
	return render(request, 'big/index.html', {
		'posts': posts,
	})

def category(request, slug):
	cat = Category.objects.get(slug=slug)
	posts = Article.objects.filter(category__slug=slug)
	return render(request, 'big/category.html', {
		'cat': cat,
		'posts': posts,
	})

def article(request, slug):
	post = Article.objects.get(slug=slug)
	return render(request, 'big/article.html', {
		'post': post,
	})

def publication(request, slug):
	research = Publication.objects.get(slug=slug)
	return render(request, 'big/publication.html', {
		'research': research,
	})

def publications(request):
	researches = Publication.objects.all()
	return render(request, 'big/publications.html', {
		'researches': researches,
	})

