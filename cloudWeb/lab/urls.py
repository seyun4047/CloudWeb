from django.urls import path
from django.contrib.auth import views
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'lab'

urlpatterns = [
    path('', views.main, name='lab'),
    path('filmgen/', views.filmgen, name='filmgen'),
    path('filmup/', views.upload_film_image, name='upload_film_image'),
    # path('logout/', views.logout_view, name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)