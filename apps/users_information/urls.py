from django.urls import path
from  . views import UploadCvView 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'apps.users_information'


urlpatterns = [
    path('uploads-cv/', UploadCvView.as_view(), name='upload_cv'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)