from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="adminpanel"),
    path('logout/', views.admin_logout, name='admin-logout'),
    path('login/', views.admin_login, name='admin-login'),
    path('tutorials/', views.Tutorials.as_view(), name='admin-tutorials'),
    path('catagories/', views.Catagories.as_view(), name='admin-catagories'),
    path('users/', views.Users.as_view(), name='admin-users'),
]