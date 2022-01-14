from django.urls.conf import path
from . import views

app_name = "image"
urlpatterns = [
    path("", views.index, name="index"),
    path("reshape/", views.reshape, name="reshape"),
    path("resize/", views.resize, name="resize"),
    path("reformat/", views.reformat, name="reformat"),
]
