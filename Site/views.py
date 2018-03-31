from django.shortcuts import render
from django.views import generic

from .models import File
from django.core.files.storage import FileSystemStorage



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


def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload.html', )
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
