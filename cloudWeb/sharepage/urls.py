from django.urls import path
from . import views
from django.conf import settings
from .views import upload_images, delete_image, download_image, delete_list, download_list, upload_our_images, delete_our_image, download_our_image, delete_our_list, download_our_list
from django.conf.urls.static import static
urlpatterns = [
    path('',views.PostList.as_view(), name='post_list'),
    path('upload/',upload_images, name='upload_images'),
    path('delete_list/', delete_list, name='delete_list'),
    path('download_list/', download_list, name='download_list'),
    path('download_image/<int:pk>', download_image, name='download_image'),
    path('delete_image/<int:pk>', delete_image, name='delete_image'),
    path('ourimg/', views.OurList.as_view(), name='our_list'),
    #     upload_our_images
    path('uploadourimg/', upload_our_images, name='upload_our_images'),
    path('delete_our_list/', delete_our_list, name='delete_our_list'),
    path('download_our_list/', download_our_list, name='download_our_list'),
    path('download_our_image/<int:pk>', download_our_image, name='download_our_image'),
    path('delete_our_image/<int:pk>', delete_our_image, name='delete_our_image'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)