from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.


def user_directory_path(instance, filename):
    return 'user_{0}/{1}/{2}'.format(instance.user, type(instance), filename)


class Recourse(models.Model):
    file=models.FileField(upload_to=user_directory_path)
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
