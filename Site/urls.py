from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^file/(?P<pk>\d+)$', views.file_detail_view, name='file-detail'),
]