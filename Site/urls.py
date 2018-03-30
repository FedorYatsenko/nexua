from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^my_files$', views.MyFilesListView.as_view(), name='my_files'),
    url(r'^random_files$', views.RandomFilesListView.as_view(), name='random_files'),
    url(r'^new_random_files/', views.NewRandomFilesListView.as_view(), name='new_random_files'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^file/(?P<pk>\d+)$', views.file_detail_view, name='file-detail'),
]