from django.conf.urls import url, include

from . import views


urlpatterns = [
	url(r'^$', views.index, name='tnb_index'),
	url(r'^music/', include('tnb_music.urls')),
]
