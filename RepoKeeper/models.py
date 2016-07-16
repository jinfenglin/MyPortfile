from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import os

# Create your models here.


def user_directory_path(instance, filename):
    return 'user_{0}/{1}/{2}'.format(instance.user, type(instance), filename)


class Recourse(models.Model):
    MEDIA_CHOICE=(('AUDIO','audio'),
                  ('TEXT','text'),
                  ('IMAGE','image'),
                  ('VIDEO','video'),
                  ('UNKNOWN','unknown'))

    file=models.FileField(upload_to=user_directory_path)
    media_type= models.CharField(max_length=100,choices=MEDIA_CHOICE,default="UNKNOWN")
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)

    def getFileName(self):
        return os.path.basename(self.file.name)