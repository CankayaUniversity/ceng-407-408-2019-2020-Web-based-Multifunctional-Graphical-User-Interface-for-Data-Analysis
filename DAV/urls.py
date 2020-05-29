from django.urls import path
from . import views
from DAV.dash_apps.finished_apps import SimpleExample

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('DAV/',views.analysisView,name='analysis'),
    path('upload/',views.upload_file,name='upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
