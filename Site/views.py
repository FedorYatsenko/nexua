from django.shortcuts import render
from django.views import generic

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


def handle_uploaded_file(request):
    save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', request.FILES.get('file'))
    path = default_storage.save(save_path, request.FILES.get('file'))


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        uploaded_file = File()
        # uploaded_file.file_itself = form.cleaned_data.get('file')
        uploaded_file.file_itself = request.POST.get('file')
        uploaded_file.upload_date = datetime.datetime.now()
        # uploaded_file.size = form.cleaned_data.get('file').size
        uploaded_file.size = 100
        uploaded_file.path_on_disk = 'D:\\nexua_files'
        uploaded_file.link = 'abclink'
        uploaded_file.file_type = 'txt'
        uploaded_file.file_name = 'newfile1'
        uploaded_file.time_to_live = datetime.timedelta(days=2)
        uploaded_file.user = request.user
        uploaded_file.save()
        handle_uploaded_file(request.FILES.get('file'))



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
