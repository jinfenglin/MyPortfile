from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import datetime
#from django.contrib.postgres.fields import JSONField
# Create your models here.

#use django.contrib.auth.get_user_model() to refer to the current active user in code, rather than User

def user_directory_path(instance,filename):
        return 'user_{0}/{1}/{2}'.format(instance.user,type(instance),filename)

class Profile(models.Model):
    avatar = models.ImageField(upload_to=user_directory_path)
    activation_key=models.CharField(max_length=40,null=True)
    key_expires=models.DateTimeField(default=datetime.datetime.now)
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)

class Masterpiece(models.Model):
    layout=models.FileField(upload_to=user_directory_path)
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)

 
