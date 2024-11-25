from django.contrib import admin
from django.urls import path
from backend.views import HomePage, upload_image, ShowImageView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='home'),
    path('upload/', upload_image, name='upload_image'),
    path('show_image/', ShowImageView.as_view(), name='show_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)