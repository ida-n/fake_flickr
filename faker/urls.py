from django.conf.urls import url, include
from . import views

app_name = 'faker'
urlpatterns = [
	#url(r'^', include('django.contrib.auth.urls')),
	url(r'^$', views.index, name='index'),
	url(r'^images/$', views.images, name='images'),
	url(r'^my_images/$', views.my_images, name='my_images'),
	url(r'^my_images/upload$', views.upload, name='upload'),
	url(r'^images/(?P<image_id>[0-9]+)/$', views.image, name='image'),
	url(r'^images/(?P<image_id>[0-9]+)/vote/$', views.vote, name='vote'),
]