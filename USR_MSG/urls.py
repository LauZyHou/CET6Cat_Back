from USR_MSG import views
from django.urls import path

urlpatterns = [
    path(r'add_user', views.add_user),
    path(r'get_users', views.get_users)
]
