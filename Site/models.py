from django.db import models
from django.contrib.auth.models import User
import uuid
from django.urls import reverse


# Create your models here.

class File(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    file_name = models.CharField(max_length=50, help_text="Enter file name", verbose_name="File name")
    upload_date = models.DateTimeField(verbose_name="Date of file upload")
    link = models.CharField(max_length=50, verbose_name="Link to file")
    path_on_disk = models.CharField(max_length=50, verbose_name="Path on disk")
    time_to_live = models.DurationField()
    file_type = models.CharField(max_length=50, help_text="Enter file type", verbose_name="File type")
    size = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    file_itself = models.FileField()

    def __str__(self):
        return 'id: %s  name: %s date: %s type: %s size: %s user: %s' % (self.id, self.file_name, self.upload_date, self.file_type, self.size, self.user.__str__())

    def get_absolute_url(self):
        return reverse('file-detail', args=[str(self.id)])

