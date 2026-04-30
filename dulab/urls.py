from django.urls import path
from .views import *
from . import views

app_name = 'dulab'

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('post/<slug:slug>.html', PostDetailView.as_view(), name='post'),
	path('news', NewsListView.as_view(), name='news'),
	path('publication', PublicationListView.as_view(), name='publication'),
	path('research', ResearchListView.as_view(), name='research'),
	path('softwares', SoftwareListView.as_view(), name='softwares'),
	path('software/<slug:slug>', SoftwareDetailView.as_view(), name='software'),
	path('member', MemberListView.as_view(), name='members'),
	path('member/<slug:slug>', MemberDetailView.as_view(), name='member'),
	path('page/<slug:slug>', PageDetailView.as_view(), name='page'),
	path('about', AboutDetailView.as_view(), name='about'),
	path('joinus', JoinusDetailView.as_view(), name='joinus'),
	path('contact', ContactDetailView.as_view(), name='contact'),
	path('signout', signout, name='signout'),
	path('signup', SignupView.as_view(), name='signup'),
	path('signin', SigninView.as_view(), name='signin'),
	path('profile', ProfileView.as_view(), name='profile'),
	path('avatar/upload', AvatarUploadView.as_view(), name='avatar-upload'),
	path('avatar/delete', AvatarDeleteView.as_view(), name='avatar-delete'),
	path('setpasswd', PasswordSetView.as_view(), name='setpasswd'),
	path('postlist', PostListView.as_view(), name='postlist'),
	path('postadd', PostAddView.as_view(), name='postadd'),
	path('postedit/<slug:slug>', PostEditView.as_view(), name='postedit'),
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