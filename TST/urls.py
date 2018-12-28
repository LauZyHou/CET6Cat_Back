from TST import views
from django.urls import path

"""
仅供测试用!
"""

urlpatterns = [
    path(r'add_user', views.add_user),
    path(r'get_users', views.get_users)
]
