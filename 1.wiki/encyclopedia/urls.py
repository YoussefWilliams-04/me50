from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>",views.entry,name="entry")
    ,path("search",views.search, name="search"),
    path("add",views.add , name="add"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("random_entry", views.random_entry, name="random_entry")
]
