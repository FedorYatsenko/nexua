from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import random
from django.core.files import File as StandartFile

from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q

from .models import File, User
from django.core.files.storage import FileSystemStorage
import datetime
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.db.models import Sum

from django.http import HttpResponse

from Site.forms import SignUpForm, LoginRestoreForm


def health(request):
    return HttpResponse(0)

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from Site.tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login


def index(request):
    files_count = File.objects.all().count()
    available_files_count = File.objects.filter(
        Q(time_to_live__isnull=True) | Q(time_to_live__gt=timezone.now())).count()
    user_count = User.objects.all().count()
    dc_total_file_size = File.objects.all().aggregate(total_file_size=Sum('size'))

    time_hour = timezone.now() + timedelta(hours=1)
    files_count_hour = File.objects.filter(time_to_live__isnull=False,
                                           time_to_live__gt=timezone.now(),
                                           time_to_live__lt=time_hour
                                           ).count()
    time_day = timezone.now() + timedelta(days=1)
    files_count_day = File.objects.filter(time_to_live__isnull=False,
                                          time_to_live__gt=timezone.now(),
                                          time_to_live__lt=time_day
                                          ).count()
    time_week = timezone.now() + timedelta(weeks=1)
    files_count_week = File.objects.filter(time_to_live__isnull=False,
                                           time_to_live__gt=timezone.now(),
                                           time_to_live__lt=time_week
                                           ).count()
    time_month = timezone.now() + timedelta(days=30)
    files_count_month = File.objects.filter(time_to_live__isnull=False,
                                            time_to_live__gt=timezone.now(),
                                            time_to_live__lt=time_month
                                            ).count()
    time_year = timezone.now() + timedelta(days=364)
    files_count_year = File.objects.filter(time_to_live__isnull=False,
                                           time_to_live__gt=timezone.now(),
                                           time_to_live__lt=time_year
                                           ).count()

    last_files = File.objects.filter(
        Q(time_to_live__isnull=True) | Q(time_to_live__gt=timezone.now())
    ).order_by('-upload_date')[:2]

    return render(
        request,
        'index.html',
        context={'files_count': files_count,
                 'available_files_count': available_files_count,
                 'user_count': user_count,
                 'total_file_size': dc_total_file_size['total_file_size'],
                 'files_count_hour': files_count_hour,
                 'files_count_day': files_count_day,
                 'files_count_week': files_count_week,
                 'files_count_month': files_count_month,
                 'files_count_year': files_count_year,
                 'object_list': last_files,
                 },
    )


def file_detail_view(request, pk):
    file = File.objects.get(pk=pk)

    return render(
        request,
        'common/download.html',
        context={'file': file}
    )


@login_required
def profile(request):
    files_count = File.objects.filter(user=request.user).count()
    available_files_count = File.objects.filter(Q(time_to_live__isnull=True) | Q(time_to_live__gt=timezone.now()),
                                                user=request.user).count()
    last_files = File.objects.filter(user=request.user).order_by('-upload_date')[:2]

    return render(
        request,
        'userpage/profile.html',
        context={'files_count': files_count,
                 'available_files_count': available_files_count,
                 'object_list': last_files, },
    )


@login_required
def upload(request):
    if request.method == 'POST':
        uploaded_file = File()
        uploaded_file.file_itself = request.FILES['file']
        uploaded_file.upload_date = timezone.now()
        uploaded_file.size = StandartFile(request.FILES['file']).size

        uploaded_file_name = StandartFile(request.FILES['file']).name
        filename, file_extension = os.path.splitext(uploaded_file_name)

        uploaded_file.file_name = filename
        uploaded_file.file_type = file_extension[1:]
        uploaded_file.user = request.user
        uploaded_file.save()

        file_url = uploaded_file.get_absolute_url()

        selected_ttl = request.POST.get('ttl')
        delete_date = timezone.now()

        if (selected_ttl == "none"):
            delete_date = None

        if (selected_ttl == "hour"):
            delete_date += datetime.timedelta(hours=1)

        if (selected_ttl == "day"):
            delete_date += datetime.timedelta(days=1)

        if (selected_ttl == "week"):
            delete_date += datetime.timedelta(weeks=1)

        if (selected_ttl == "month"):
            delete_date += datetime.timedelta(days=30)

        if (selected_ttl == "year"):
            delete_date += datetime.timedelta(days=365)

        uploaded_file.time_to_live = delete_date
        uploaded_file.save()

        return render(
            request,
            'userpage/upload.html',
            context={
                'file_name': uploaded_file_name,
                'file_url': file_url,
            },
        )
    return render(
        request,
        'userpage/upload.html',
        context={},
    )


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your nex.ua Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(
        request,
        'account_activation_sent.html',
        context={},
    )


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('profile')
    else:
        return render(request, 'account_activation_invalid.html')


def login_restore_sent(request):
    return render(
        request,
        'login_restore_sent.html',
        context={},
    )


def login_restore(request):
    if request.method == 'POST':
        form = LoginRestoreForm(request.POST)
        if form.is_valid():
            try:
                users = User.objects.get(email=form.cleaned_data['email'])

                subject = 'Restore Your nex.ua username'
                message = render_to_string('login_restore_email.html', {
                    'fullname': users.get_full_name(),
                    'login': users.username,
                })
                users.email_user(subject, message)
                return redirect('login_restore_sent')
            except User.DoesNotExist:
                form.add_error("email", "User with such email not found")
    else:
        form = LoginRestoreForm()

    return render(request, 'login_restore.html', {'form': form})


class MyFilesListView(LoginRequiredMixin, generic.ListView):
    model = File
    paginate_by = 2
    template_name = 'userpage/my_files.html'

    def get_queryset(self):
        return File.objects.filter(Q(time_to_live__isnull=True) | Q(time_to_live__gt=timezone.now()),
                                   user=self.request.user)


class RandomFilesListView(generic.ListView):
    model = File
    template_name = 'common/random_file.html'

    def get_queryset(self):
        return File.objects.filter(
            Q(time_to_live__isnull=True) | Q(time_to_live__gt=timezone.now())).order_by('?')[:2]


class NewRandomFilesListView(generic.ListView):
    model = File
    template_name = 'common/new_random_files.html'

    def get_queryset(self):
        ttl = self.request.GET.get('ttl')

        if ttl:
            if ttl == "hour":
                time_hour = timezone.now() + timedelta(hours=1)
                return File.objects.filter(time_to_live__isnull=False,
                                           time_to_live__gt=timezone.now(),
                                           time_to_live__lt=time_hour
                                           ).order_by('?')[:2]
            elif ttl == "day":
                time_day = timezone.now() + timedelta(days=1)
                return File.objects.filter(time_to_live__isnull=False,
                                           time_to_live__gt=timezone.now(),
                                           time_to_live__lt=time_day
                                           ).order_by('?')[:2]
            elif ttl == "week":
                time_week = timezone.now() + timedelta(weeks=1)
                return File.objects.filter(time_to_live__isnull=False,
                                           time_to_live__gt=timezone.now(),
                                           time_to_live__lt=time_week
                                           ).order_by('?')[:2]
            else:
                return File.objects.filter(
                    Q(time_to_live__isnull=True) | Q(time_to_live__gt=timezone.now())).order_by('?')[:2]


class NewLastFilesListView(generic.ListView):
    model = File
    template_name = 'common/new_random_files.html'

    def get_queryset(self):
        start_index = int(self.request.GET.get('index'))

        return File.objects.filter(
            Q(time_to_live__isnull=True) | Q(time_to_live__gt=timezone.now())
        ).order_by('-upload_date')[start_index:(start_index + 2)]
