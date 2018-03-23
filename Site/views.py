from django.shortcuts import render
from django.views import generic

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