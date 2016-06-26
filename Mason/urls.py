from django.conf.urls import url
from views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns =[
        url(r'^$',HomePage.as_view(),name='editor'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)