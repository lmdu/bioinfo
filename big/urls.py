# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('article/<slug>', views.article, name='article'),
	path('category/<slug>', views.category, name='category'),
	path('publication', views.publications, name='publications'),
	path('publication/<slug>', views.publication, name='publication'),
]