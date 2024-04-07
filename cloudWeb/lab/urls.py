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
    path('imgstack/', views.imgStack, name='imgstack'),
    path('stackerup/', views.upload_ImgStacker_image, name='upload_ImgStacker_image'),
    path('qrgen/', views.qrgen, name='qrgen'),
    path('qrup/', views.upload_qr_image, name='upload_qr_image'),
    path('songqrgen/', views.songqrgen, name='songqrgen'),
    path('songqrup/', views.upload_song_qr_image, name='upload_song_qr_image'),
    path('framethememory/', views.ncutsgen, name='ncutsgen'),
    path('framethememoryup/', views.upload_ncuts_image, name='upload_ncuts_image'),
    # path('ncutsgen/', views.ncutsgen, name='ncutsgen'),
    # path('ncutsup/', views.upload_ncuts_image, name='upload_ncuts_image'),
    path('download_image/<int:pk>/<int:n>', views.download_image, name='download_image')

    # path('logout/', views.logout_view, name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)