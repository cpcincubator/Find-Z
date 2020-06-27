from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="adminpanel"),
    path('logout/', views.admin_logout, name='admin-logout'),
    path('login/', views.admin_login, name='admin-login'),
    path('tutorials/', views.Tutorials.as_view(), name='admin-tutorials'),
]