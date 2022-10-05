from django.urls import re_path, path

from . import views


app_name = 'the_clients'
urlpatterns = [

     path("", views.list_clients, name="list"),
     path("<int:pk>", views.display_client, name="display"),
     path("add", views.add_client, name="add"),
     path("update/<int:pk>", views.update_client, name="update"),


]
