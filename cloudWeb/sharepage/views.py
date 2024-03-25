from django.shortcuts import render
from django.views.generic import ListView,DetailView, CreateView
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post
import requests
from .models import OurPost
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
import io
import zipfile
import cv2
from . import imgResizing
# Create your views here.
class PostList(ListView):
    model = Post
    ordering = '-pk'
    # template_name = 'blog/upload.html'
    # context_object_name = 'post_list1'


# ori_url_split =  film_ori_image_url.split('.')
#         film_image_url = ori_url_split[0] + "_gen." + ori_url_split[1]
# def upload_images(request):
#     # post = Post.objects.get(pk=post_id)
#     if request.method == 'POST' and request.FILES.getlist('images'):
#         images = request.FILES.getlist('images')
#         for image in images:
#             # 이미지를 저장하거나 원하는 처리를 수행합니다.
#             p=Post.objects.create(image=image)
#             # cv2.imread(image)
#             imgResizing.resizeImg(p.image.path)
#         return render(request, 'sharepage/form.html')
#
#     return render(request, 'sharepage/form.html')

def upload_images(request):
    # post = Post.objects.get(pk=post_id)
    if request.method == 'POST' and request.FILES.getlist('images'):
        images = request.FILES.getlist('images')
        for image in images:
            # 이미지를 저장하거나 원하는 처리를 수행합니다.
            p=Post.objects.create(image=image)
            # cv2.imread(image)
            imgResizing.resizeImg(p.image.path)
        return redirect('/gallery/cloud')

    return redirect('/gallery/cloud')

def delete_image(request, pk):
    # 요청한 포스트를 가져오거나 404 에러를 발생시킵니다.
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/gallery/cloud')
def download_image(request, pk):
    # 해당 모델 객체를 가져옵니다. 예를 들어 Post 모델을 사용하려면 Post 모델에 대한 import를 해야 합니다.
    file_obj = get_object_or_404(Post, pk=pk)

    # 이미지의 경로를 가져옵니다.
    image_path = file_obj.image.path

    # 파일이 존재하는지 확인합니다.
    if os.path.exists(image_path):
        # 파일이 존재하면 파일을 열어서 응답 객체로 반환합니다.
        with open(image_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(image_path)}"'
            return response
    else:
        # 파일이 존재하지 않으면 404 에러를 반환합니다.
        return HttpResponse(status=404)

# zip 반환
def download_list(request):
    if request.method == 'POST':
        selected = request.POST.getlist('check_list')
        print("downloadlist!!!!!!!!!!!!!!!!!!!!!!!!!!!!", selected)

        # 이미지 데이터를 저장할 리스트
        image_data_list = []

        for pk in selected:
            file_obj = get_object_or_404(Post, pk=pk)
            image_path = file_obj.image.path
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    # 이미지 데이터를 읽어서 리스트에 추가
                    image_data_list.append(f.read())
            else:
                # 해당 이미지가 존재하지 않을 경우 다음 이미지로 넘어감
                continue

        # 모든 이미지 데이터를 하나의 응답으로 반환
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for index, image_data in enumerate(image_data_list):
                zip_file.writestr(f'image_{index + 1}.jpg', image_data)

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="downloaded_images.zip"'

        return response

    return redirect('/gallery/cloud')

def delete_list(request):
    if request.method == 'POST':
        selected = request.POST.getlist('check_list')
        print("deletelist!!!!!!!!!!!!!!!!!!!!!!!!!!!!", selected)
        for pk in selected:
            delete_image(request, pk)
    return redirect('/gallery/cloud')



# ---------------------------- ourlist

def upload_our_images(request):
    # post = Post.objects.get(pk=post_id)
    if request.method == 'POST' and request.FILES.getlist('images'):
        images = request.FILES.getlist('images')
        for image in images:
            # 이미지를 저장하거나 원하는 처리를 수행합니다.
            p=OurPost.objects.create(image=image)
            # cv2.imread(image)
            imgResizing.resizeOURImg(p.image.path)
        return redirect('/gallery')

    return redirect('/gallery')

def delete_our_image(request, pk):
    # 요청한 포스트를 가져오거나 404 에러를 발생시킵니다.
    post = get_object_or_404(OurPost, pk=pk)
    post.delete()
    return redirect('/gallery')

def download_our_image(request, pk):
    # 해당 모델 객체를 가져옵니다. 예를 들어 Post 모델을 사용하려면 Post 모델에 대한 import를 해야 합니다.
    file_obj = get_object_or_404(OurPost, pk=pk)

    # 이미지의 경로를 가져옵니다.
    image_path = file_obj.image.path

    # 파일이 존재하는지 확인합니다.
    if os.path.exists(image_path):
        # 파일이 존재하면 파일을 열어서 응답 객체로 반환합니다.
        with open(image_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(image_path)}"'
            return response
    else:
        # 파일이 존재하지 않으면 404 에러를 반환합니다.
        return HttpResponse(status=404)

# zip 반환
def download_our_list(request):
    if request.method == 'POST':
        selected = request.OurPost.getlist('check_list')
        print("downloadlist!!!!!!!!!!!!!!!!!!!!!!!!!!!!", selected)

        # 이미지 데이터를 저장할 리스트
        image_data_list = []

        for pk in selected:
            file_obj = get_object_or_404(OurPost, pk=pk)
            image_path = file_obj.image.path
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    # 이미지 데이터를 읽어서 리스트에 추가
                    image_data_list.append(f.read())
            else:
                # 해당 이미지가 존재하지 않을 경우 다음 이미지로 넘어감
                continue

        # 모든 이미지 데이터를 하나의 응답으로 반환
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for index, image_data in enumerate(image_data_list):
                zip_file.writestr(f'image_{index + 1}.jpg', image_data)

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="downloaded_images.zip"'

        return response

    return redirect('/gallery')

def delete_our_list(request):
    if request.method == 'POST':
        selected = request.OurPost.getlist('check_list')
        print("deletelist!!!!!!!!!!!!!!!!!!!!!!!!!!!!", selected)
        for pk in selected:
            delete_image(request, pk)
    return redirect('/gallery')

class OurList(ListView):
    model = OurPost
    ordering = '-pk'
    template_name = 'sharepage/our_list.html'
    context_object_name = 'our_list'


