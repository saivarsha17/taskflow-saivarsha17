from django.urls import include, path

urlpatterns = [
    path("auth/", include("auth.urls")),
    path("", include("tasks.urls")),
]
