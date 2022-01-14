from django.urls.conf import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "image"
urlpatterns = [
    path("", views.index, name="index"),
    path("reshape/", views.reshape, name="reshape"),
    path("resize/", views.resize, name="resize"),
    path("reformat/", views.reformat, name="reformat"),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
