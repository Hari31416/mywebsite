from . import views
from django.urls.conf import path

app_name = "youtube"
urlpatterns = [
    path("", views.index, name="index"),
    path("download/", views.download, name="download"),
]
