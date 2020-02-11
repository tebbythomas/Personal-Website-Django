from django.db import models

# Create your models here.
class PersonalDetails(models.Model):
    headline = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    email = models.CharField(max_length=100) 
    profile_pic = models.ImageField(upload_to='projects_photos/')
    resume = models.FileField(upload_to='resume/')