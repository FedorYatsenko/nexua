from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

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


@login_required
def profile(request):
    files_count = File.objects.filter(user=request.user).count()
    last_files = File.objects.filter(user=request.user).order_by('-upload_date')[:2]

    return render(
        request,
        'userpage/profile.html',
        context={'files_count': files_count, 'last_files': last_files, },
    )


class MyFilesListView(LoginRequiredMixin, generic.ListView):
    model = File
    paginate_by = 2
    template_name = 'userpage/my_files.html'

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)


class RandomFilesListView(generic.ListView):
    model = File
    template_name = 'common/random_file.html'

    def get_queryset(self):
        return File.objects.filter().order_by('?')[:2]


class NewRandomFilesListView(generic.ListView):
    model = File
    template_name = 'common/new_random_files.html'

    def get_queryset(self):
        ttl = self.request.GET.get('ttl')

        if ttl:
            if ttl == "hour":
                time_hour = datetime.now() + timedelta(hours=1)
                return File.objects.filter(time_to_live__isnull=False, time_to_live__lt=time_hour).order_by('?')[:2]
            elif ttl == "day":
                time_hour = datetime.now() + timedelta(days=1)
                return File.objects.filter(time_to_live__isnull=False, time_to_live__lt=time_hour).order_by('?')[:2]
            elif ttl == "week":
                time_hour = datetime.now() + timedelta(weeks=1)
                return File.objects.filter(time_to_live__isnull=False, time_to_live__lt=time_hour).order_by('?')[:2]
            else:
                return File.objects.filter().order_by('?')[:2]