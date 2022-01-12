from django.urls.conf import path
from . import views

app_name = "language"
urlpatterns = [
    path("", views.index, name="index"),
    path("help/", views.help, name="help"),
    # path("result/", views.result, name="result"),
]
