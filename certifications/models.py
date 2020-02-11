from django.db import models

# Create your models here.
class Certificate(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.name