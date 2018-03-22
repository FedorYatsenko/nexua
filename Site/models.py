from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    file_name = models.CharField(max_length=50, help_text="Enter file name", verbose_name="File name")
    upload_date = models.DateTimeField(verbose_name="Date of file upload")
    link = models.CharField(max_length=50, verbose_name="Link to file")
    path_on_disk = models.CharField(max_length=50, verbose_name="Path on disk")
    time_to_live = models.DurationField()
    file_name = models.CharField(max_length=50, help_text="Enter file name", verbose_name="File type")
    size = models.AutoField()
    user = models.ForeignKey(User, unique=True)

