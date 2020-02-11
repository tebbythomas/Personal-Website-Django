from django.db import models

# Create your models here.
class Portfolio(models.Model):
    title = models.CharField(max_length=200)
    github_link = models.CharField(max_length=200)
    demo_link = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    project_image = models.ImageField(upload_to='projects_photos/')
    def __str__(self):
        return self.title
    