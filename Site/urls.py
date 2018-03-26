from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^my_files$', views.MyFilesListView.as_view(), name='my_files'),
    url(r'^file/(?P<pk>\d+)$', views.file_detail_view, name='file-detail'),
]