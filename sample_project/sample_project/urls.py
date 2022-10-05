from django.contrib import admin
from django.urls import path, include
from .api import api
urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("the_clients.urls")),
    path('accounts/', include('allauth.urls')),
     path("api/", api.urls, name="api")
]
