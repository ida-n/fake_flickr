from django.conf.urls import url
from . import views

app_name = 'faker'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^images/$', views.images, name='images'),
	url(r'^images/(?P<image_id>[0-9]+)/$', views.image, name='image'),
	url(r'^images/(?P<image_id>[0-9]+)/vote/$', views.vote, name='vote'),
]