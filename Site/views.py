from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import random
from django.core.files import File as StandartFile

from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q

from .models import File
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
import datetime
import os
from django.core.files.storage import default_storage
from django.conf import settings



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


def handle_uploaded_file(f, path):
    with open(path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

  
"""
def handle_uploaded_file(request):
    save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', request.FILES.get('file'))
    path = default_storage.save(save_path, request.FILES.get('file'))
"""


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        uploaded_file = File()
        uploaded_file.file_itself = request.FILES['file']
       # uploaded_file.upload_date = datetime.datetime.now(timezone.now().tzinfo)
        uploaded_file.upload_date = timezone.now()
        uploaded_file.size = StandartFile(request.FILES['file']).size
        rand_id = str(random.randint(0, 10000))
        uploaded_file_name = StandartFile(request.FILES['file']).name
        filename, file_extension = os.path.splitext(uploaded_file_name)
        uploaded_file.path_on_disk = "D:\\" + filename + rand_id + file_extension
        uploaded_file.link = filename + rand_id
        uploaded_file.file_name = uploaded_file_name
        uploaded_file.file_type = file_extension
        uploaded_file.time_to_live = datetime.timedelta(days=2)
        uploaded_file.user = request.user
        uploaded_file.save()
        handle_uploaded_file(request.FILES.get('file'), "D:\\" + filename + rand_id + file_extension)
        return render(
            request,
            'userpage/upload.html',
            context={},)
    return render(
        request,
        'userpage/upload.html',
        context={},
    )

# if request.method == 'POST' and request.FILES['myfile']:
    #     myfile = request.FILES['myfile']
    #     fs = FileSystemStorage()
    #     filename = fs.save(myfile.name, myfile)
    #     uploaded_file_url = fs.url(filename)
    #     return render(request, 'upload.html', {
    #         'uploaded_file_url': uploaded_file_url
    #     })


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
                return File.objects.filter(time_to_live__isnull=False,
                                           time_to_live__gt=datetime.now(),
                                           time_to_live__lt=time_hour
                                           ).order_by('?')[:2]
            elif ttl == "day":
                time_day = datetime.now() + timedelta(days=1)
                return File.objects.filter(time_to_live__isnull=False,
                                           time_to_live__gt=datetime.now(),
                                           time_to_live__lt=time_day
                                           ).order_by('?')[:2]
            elif ttl == "week":
                time_week = datetime.now() + timedelta(weeks=1)
                return File.objects.filter(time_to_live__isnull=False,
                                           time_to_live__gt=datetime.now(),
                                           time_to_live__lt=time_week
                                           ).order_by('?')[:2]
            else:
                return File.objects.filter(Q(time_to_live__isnull=True) | Q(time_to_live__gt=datetime.now())).order_by('?')[:2]
