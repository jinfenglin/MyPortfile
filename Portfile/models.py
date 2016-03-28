from __future__ import unicode_literals

from django.db import models
#from django.contrib.postgres.fields import JSONField
# Create your models here.

def user_directory_path(instance,filename):
        return 'user_{0}/{1}/{2}'.format(instance.owner_id,type(instance),filename)

class User(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    register_date=models.DateField(auto_now_add=True)

class Masterpiece(models.Model):
    layout=models.FileField(upload_to=user_directory_path)
    user_id=models.ForeignKey(User)
class Video(models.Model):
    video=models.FileField(upload_to=user_directory_path)
    owner_id=models.ForeignKey(User)
class Image(models.Model):
    video=models.ImageField(upload_to=user_directory_path)
    owner_id=models.ForeignKey(User)
    
