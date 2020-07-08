from django.urls import path
from . import views
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<slug:root_slug>', views.Catagories.as_view(), name='catagories'),
    path('<slug:root_slug>/<slug:catagory_slug>', views.Tutorials.as_view(), name='tutorials'),
]