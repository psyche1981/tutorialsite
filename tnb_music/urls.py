from django.conf.urls import url

from . import views


urlpatterns = [
	# /tnb/music
	url(r'^$', views.index, name='tnb_music_index'),

	# /tnb/music/(album_id)
	url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='tnb_music_detail'),
]
