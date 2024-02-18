from django.urls import path
from . import views
from django.conf import settings
from .views import upload_images, delete_image, download_image, delete_list, download_list
from django.conf.urls.static import static
urlpatterns = [
    path('',views.PostList.as_view(), name='post_list'),
    path('upload/',upload_images, name='upload_images'),
    path('delete_image/<int:pk>', delete_image),
    path('delete_list/', delete_list, name='delete_list'),
    path('download_list/', download_list, name='download_list'),
    path('download_image/<int:pk>', download_image)
               ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)