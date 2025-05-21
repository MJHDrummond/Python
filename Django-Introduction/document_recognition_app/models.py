from django.db import models
from django.utils import timezone

class FileReaderModel(models.Model):
    file_name = models.CharField(max_length=100)
    file = models.FileField()
    file_body = models.TextField()
    date_read = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_read']
        verbose_name_plural = "FileReaderModel"

    def __str__(self):
        return str(self.file_name) + " File"