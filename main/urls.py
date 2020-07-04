from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.Index.as_view(), name='index'),
    path('', views.Academic.as_view(), name='academic'),
    path('programming/', views.Programming.as_view(), name='programming'),
    path('devops/', views.Devops.as_view(), name='devops'),
]