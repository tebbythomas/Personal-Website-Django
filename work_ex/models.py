from django.db import models
from datetime import datetime
# Create your models here.
class WorkEx(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    end_date = models.DateTimeField(default=datetime.now, blank=True)
    present_job = models.BooleanField(default=False)
    def __str__(self):
        return self.title