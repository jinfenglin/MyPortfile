from django.conf.urls import url
from views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('^$',ManagePage.as_view(),name='manage'),
    url('^upload$',None,name='upload'), #end point for uploading files, accept ajax request as well

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
