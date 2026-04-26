from django.urls import path
from .views import *
from . import views

app_name = 'dulab'

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('post/<slug:slug>.html', PostDetailView.as_view(), name='post'),
	path('news', PostListView.as_view(), name='news'),
	path('publication', PublicationListView.as_view(), name='publication'),
	path('research', ResearchListView.as_view(), name='research'),
	path('softwares', SoftwareListView.as_view(), name='softwares'),
	path('software/<slug:slug>', SoftwareDetailView.as_view(), name='software'),
	path('member', MemberListView.as_view(), name='members'),
	path('member/<slug:slug>', MemberDetailView.as_view(), name='member'),
	path('page/<slug:slug>', PageDetailView.as_view(), name='page'),
	path('signout', SignoutView.as_view(), name='signout'),
	path('about', AboutDetailView.as_view(), name='about'),
	path('joinus', JoinusDetailView.as_view(), name='joinus'),
	path('contact', ContactDetailView.as_view(), name='contact'),
	#path('signin', views.signin, name='signin'),
	#path('signout', views.signout, name='signout'),
	#path('signup', views.signup, name='signup'),
	#path('profile', views.profile, name='profile'),
	#path('resetpasswd', views.resetpasswd, name='resetpasswd'),
	#path('upload', views.upload, name='upload'),
	#path('browser', views.browser, name='browser'),
	#path('fund', views.fund, name='fund'),
	#path('expense/<fid>', views.expense, name='expense')
]