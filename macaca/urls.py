# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('organism/', views.organism, name='organism'),
	path('species/<int:sid>', views.species, name='species'),
	path('group/<int:gid>', views.group, name='group'),
	path('variants/', views.variants, name='variants'),
	path('variants/<gid>', views.snpcds, name='snpcds'),
	path('nrsnps/', views.nrsnps, name='nrsnps'),
	path('specific/', views.specific, name='specific'),
	path('snp/<int:sid>/', views.snp, name='snp'),
	re_path(r'^snp/MACSNP(?P<indiv>[0-9]{3})(?P<sid>[0-9]{9})/$', views.snpid, name='snpid'),
	re_path(r'^snp/MACSNP(?P<cat>[GS])(?P<cid>[0-9]{2})(?P<sid>[0-9]{9})/$', views.snpspec, name='snpspec'),
	path('search/', views.search, name='search'),
	path('retrieve/', views.retrieve, name='retrieve'),
	path('download/', views.download, name='download'),
	path('gene/<gid>', views.gene, name='gene'),
	path('pileup/<int:sid>', views.pileup, name='pileup'),
	path('statistics/', views.statistics, name='statistics'),
	path('drugs/', views.drugs, name='drugs'),
	path('drugs/<did>', views.drug, name='drug'),
	path('diseases/', views.diseases, name='diseases'),
	path('diseases/<did>', views.disease, name='disease'),
]