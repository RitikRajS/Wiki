from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"), 
    path("search", views.search, name="search"),
    path("random_page", views.random_page, name ="random_page"), 
    path("new_page", views.new_page, name="new_page"),
    path("edit/<str:title>", views.edit, name="edit")
]

