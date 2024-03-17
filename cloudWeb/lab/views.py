import os

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, ImgStackerPost, QRPost
from .forms import PostForm
import requests
from .FilmGen import FilmGen
from .FilmGen import FilmGen2
from .QRGen import QRGenerator
from .ImgStacker import ImgStacker
# Create your views here.
def main(request):
    print("here, lab")
    return render(request, 'lab/lab_main.html')

def filmgen(request):
    print("here, filmgen")
    return render(request, 'lab/film/filmgen.html')
    # return render(request, 'lab/form.html')

# def hi(request):
#     if request.method == 'POST':
#         print("hello")

# # Filmgen1
# def upload_film_image(request):
#     # post = Post.objects.get(pk=post_id)
#     if request.method == 'POST' and request.FILES.get('film_image'):
#         image = request.FILES.get('film_image')
#         p = Post.objects.create(image=image)
#         print("img saved: ", p.image.path)
#         #filmgen
#         try:
#             FilmGen.gen(p.image.path)
#         except Exception:
#             return render(request, 'lab/film/filmError.html')
#         # FilmGen.gen(p.get_img_src())
#         film_ori_image_url = p.image.url  # 이미지의 URL을 가져옴
#         ori_url_split =  film_ori_image_url.split('.')
#         film_image_url = ori_url_split[0] + "_gen." + ori_url_split[1]
#         return render(request, 'lab/film/filmgened.html', {'film_image_url': film_image_url, 'film_ori_image_url': film_ori_image_url})
#         # return render(request, 'lab/film/filmgened.html')
#     print("film_gen_error")
#     return render(request, 'lab/film/filmgen.html')

# FilmGen2
def upload_film_image(request):
    # post = Post.objects.get(pk=post_id)
    if request.method == 'POST' and request.FILES.get('film_image'):
        image = request.FILES.get('film_image')
        p = Post.objects.create(image=image)
        print("img saved: ", p.image.path)
        #filmgen
        try:
            FilmGen2.gen(p.image.path)
        except Exception:
            return render(request, 'lab/film/filmError.html')
        # FilmGen.gen(p.get_img_src())
        film_ori_image_url = p.image.url  # 이미지의 URL을 가져옴
        ori_url_split =  film_ori_image_url.split('.')
        film_image_url = ori_url_split[0] + "_gen." + ori_url_split[1]
        return render(request, 'lab/film/filmgened.html', {'film_image_url': film_image_url, 'film_ori_image_url': film_ori_image_url})
        # return render(request, 'lab/film/filmgened.html')
    print("film_gen_error")
    return render(request, 'lab/film/filmgen.html')

# def show_film_image(request, img_path):
#     render(request, 'lab/lab_main.html')

def imgStack(request):
    print("here, image stacker")
    return render(request, 'lab/stacker/stacker.html')

def upload_ImgStacker_image(request):
    if request.method == "POST" and request.FILES.getlist('stc_images'):
        imgs = request.FILES.getlist('stc_images')
        postedImgLst = list()
        for img in imgs:
            postedImgLst.append(ImgStackerPost.objects.create(image=img))
        print("this postedImgLst", postedImgLst)
        # stackedImgUrl = ImgStacker.imgStack(postedImgLst)
        gen = ImgStacker.imgStack(postedImgLst)
        if not gen:
            print("stacked error")
            return render(request, 'lab/stacker/stackError.html')
        else:
            generated_path_split = postedImgLst[0].image.url.split('.')
            generated_path = generated_path_split[0] + "_gen." + generated_path_split[1]
            return render(request, 'lab/stacker/stacked.html', {'stacked_image_url': generated_path, 'stacked_ori_image_url': postedImgLst[1].image.url})
    print("stacked error")
    return render(request, 'lab/stacker/stackError.html')
def qrgen(request):
    print("here, qrgen")
    return render(request, 'lab/qr/qrgen.html')
def upload_qr_image(request):
    # post = Post.objects.get(pk=post_id)
    if request.method == 'POST' and request.FILES.get('qr_image'):
        image = request.FILES.get('qr_image')
        data = request.POST.get('qr_content')
        p = QRPost.objects.create(image=image, content=data)
        print("img saved: ", p.image.path)
        try:
            print("path is", p.image.path)
            print("data:", p.content)
            QRGenerator.QRGen(p.image.path, p.content)
        except Exception as e:
            print("error:", type(e).__name__)
            return render(request, 'lab/qr/qrError.html')

        qr_ori_image_url = p.image.url  # 이미지의 URL을 가져옴
        ori_url_split = qr_ori_image_url.split('.')
        qr_image_url = ori_url_split[0] + "_qr_gen." + ori_url_split[1]
        return render(request, 'lab/qr/qrgened.html', {'qr_image_url': qr_image_url, 'pk':p.pk})
        # return render(request, 'lab/film/filmgened.html')
    print("qr_gen_error")
    return render(request, 'lab/qr/qrgen.html')

def download_image(request, pk, n):
    if n==1:
        p = Post
    elif n==2:
        p = ImgStackerPost
    elif n==3:
        p = QRPost
    # 해당 모델 객체를 가져옵니다. 예를 들어 Post 모델을 사용하려면 Post 모델에 대한 import를 해야 합니다.
    file_obj = get_object_or_404(p, pk=pk)

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
