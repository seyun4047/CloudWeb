from django.shortcuts import render, redirect, get_object_or_404
from lab.models import Post
from lab.forms import PostForm
import requests
from . import FilmGen
from django.conf import settings
# Create your views here.
def main(request):
    print("here, lab")
    return render(request, 'lab/lab_main.html')

def filmgen(request):
    print("here, filmgen")
    return render(request, 'lab/film/filmgen.html')
    # return render(request, 'lab/form.html')

def hi(request):
    if request.method == 'POST':
        print("hello")

def upload_film_image(request):
    # post = Post.objects.get(pk=post_id)
    if request.method == 'POST' and request.FILES.get('film_image'):
        image = request.FILES.get('film_image')
        p = Post.objects.create(image=image)
        print("img saved: ",p.image.path)
        #filmgen
        FilmGen.gen(p.image.path)
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