from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import File


def index(request):
    return render(
        request,
        'index.html',
        context={},
    )


def file_detail_view(request, pk):
    file_id = File.objects.get(pk=pk)

    return render(
        request,
        'common/download.html',
        context={'file': file_id, }
    )

class MyFilesListView(LoginRequiredMixin, generic.ListView):
    model = File
    paginate_by = 2
    template_name = 'userpage/my_files.html'

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)