from django.urls import path
from . import views

app_name = "map"
urlpatterns = [
    path("maps/shelters/", views.map_func, name="map-shelters"),
]
