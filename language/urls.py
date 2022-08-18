from django.urls.conf import path
from . import views

app_name = "language"
urlpatterns = [
    path("", views.index, name="index"),
]
