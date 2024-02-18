from django.shortcuts import render
from django.views.generic import ListView,DetailView, CreateView
from django.shortcuts import render, redirect, get_object_or_404

from sharepage.models import Post
import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
import io
import zipfile
# Create your views here.
class PostList(ListView):
    model = Post
    ordering = '-pk'
    # template_name = 'blog/upload.html'
    # context_object_name = 'post_list1'

def upload_images(request):
    # post = Post.objects.get(pk=post_id)
    if request.method == 'POST' and request.FILES.getlist('images'):
        images = request.FILES.getlist('images')
        for image in images:
            # 이미지를 저장하거나 원하는 처리를 수행합니다.
            Post.objects.create(image=image)
        return render(request, 'sharepage/form.html')

    return render(request, 'sharepage/form.html')

def delete_image(request, pk):
    # 요청한 포스트를 가져오거나 404 에러를 발생시킵니다.
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/')
#
# def download_image(request, pk):
#     file_obj = get_object_or_404(Post, pk=pk)
#     print("오브젝트:", file_obj)
#     file_path = os.path.join(settings.MEDIA_ROOT, str(file_obj.image))
#     print("패스:", file_path)
#     with open(file_path, 'rb') as file:
#         response = HttpResponse(file.read(), content_type='application/force-download')
#         response['Content-Disposition'] = f'attachment; filename="{file_obj.image.name}"'
#         print("리스폰스:",response)
#         return response

# # pip install requests
# def download_image(request, pk):
#     # 해당 모델 객체를 가져옵니다. 예를 들어 Post 모델을 사용하려면 Post 모델에 대한 import를 해야 합니다.
#     file_obj = get_object_or_404(Post, pk=pk)
#     print(file_obj)
#     # 이미지의 URL을 가져옵니다. 이미지가 저장된 모델 필드에 따라 다를 수 있습니다.
#     image_url = file_obj.image.url
#
#
#     # 이미지를 다운로드합니다.
#     response = requests.get(image_url)
#
#     # 다운로드된 이미지의 내용을 HttpResponse에 담아 반환합니다.
#     http_response = HttpResponse(response.content, content_type='image/jpeg')
#     http_response['Content-Disposition'] = f'attachment; filename="{file_obj.image.name}"'
#
#     return http_response


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


# def download_list(request):
#     if request.method == 'POST':
#         selected = request.POST.getlist('check_list')
#         print("downloadlist!!!!!!!!!!!!!!!!!!!!!!!!!!!!", selected)
#
#         # 선택된 이미지들을 하나씩 다운로드
#         for pk in selected:
#             file_obj = get_object_or_404(Post, pk=pk)
#             image_path = file_obj.image.path
#             if os.path.exists(image_path):
#                 with open(image_path, 'rb') as f:
#                     response = HttpResponse(f.read(), content_type='image/jpeg')
#                     response['Content-Disposition'] = f'attachment; filename="{os.path.basename(image_path)}"'
#                     # 현재 이미지를 다운로드하고 바로 반환
#                     return response
#             else:
#                 # 해당 이미지가 존재하지 않을 경우 다음 이미지로 넘어감
#                 continue
#
#     return redirect('/')

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

    return redirect('/')

def delete_list(request):
    if request.method == 'POST':
        selected = request.POST.getlist('check_list')
        print("deletelist!!!!!!!!!!!!!!!!!!!!!!!!!!!!", selected)
        for pk in selected:
            delete_image(request, pk)
    return redirect('/')

