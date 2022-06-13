from django.urls.conf import path
from . import views

app_name = "models"
urlpatterns = [
    path("", views.index, name="index"),
    path("food_vision/", views.food_vision, name="food_vision"),
]
