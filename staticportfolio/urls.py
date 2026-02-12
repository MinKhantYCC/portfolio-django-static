from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("letter-to-thon", views.valentine, name="love"),
]