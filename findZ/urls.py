from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from main import views as main_views
from account import views as account_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', main_views.search, name="search"),
    path('search/<slug:subcategory_slug>/', main_views.search_subcategory, name="search-subcategory"),
    path('course-filter/', main_views.course_filter, name='course-filter'),
    path('register/', account_views.register, name='register'),
    path('login/', account_views.login, name='login'),
    path('logout/', account_views.logout, name='logout'),
    path('profile/', account_views.profile, name='profile'),
    path('editprofile/', account_views.editprofile, name='editprofile'),
    path('editpassword/', account_views.editpassword, name='editpassword'),
    path('submission/', main_views.submit_tutorial, name='submit'),
    path('submission-criteria/', main_views.guidelines, name='guidelines'),
    path('', main_views.index, name='home'),
    path('<slug:category_slug>/', main_views.category, name='category'),
    path('<slug:category_slug>/<slug:sub_category_slug>/',
         main_views.sub_category, name='sub-category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# handler404 = main.views.not_found
