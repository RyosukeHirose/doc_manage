from django.db import models
import uuid
from django.utils import timezone

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=255)
    words_list = models.TextField(default="")
    file_path = models.CharField(default="", max_length=255)
    created_of_article = models.DateTimeField(default=timezone.now)
    url = models.TextField(default="")

    def __str__(self):
        return self.file_name

class LastFile(models.Model):
    file_name = models.CharField(max_length=255)
    last_update = models.DateTimeField(default=timezone.now)
