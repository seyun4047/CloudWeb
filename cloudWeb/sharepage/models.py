from django.db import models
from django.views.generic import ListView,DetailView, CreateView
import os
# Create your models here.
class Post(models.Model):
    # title = models.CharField(max_length=255, black=True)
    image = models.FileField(upload_to='sharepage/images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}{self.created_at}'

    def get_absolute_url(self):
        return f'/{self.pk}/'

    def delete(self, *args, **kwargs):
        # 모델이 삭제될 때 연결된 파일도 함께 삭제
        if self.image:
            # 파일 삭제
            file_path = self.image.path
            # 썸네일 파일 삭제
            file_t_path = f"{self.image.path.split('.')[0]}_t.{self.image.path.split('.')[1]}"
            if os.path.exists(file_path) and os.path.exists(file_t_path):
                os.remove(file_path)
                os.remove(file_t_path)
        super().delete(*args, **kwargs)

    # def download_image(self, id):
    #     if self.image:
    #         # 파일 다운로드
    #         file_path = self.image.path
    #         if os.path.exists(file_path):

    def get_t_url(self):
        return f"{self.image.url.split('.')[0]}_t.{self.image.url.split('.')[1]}"

class PostDetail(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        return context


class OurPost(models.Model):
    # title = models.CharField(max_length=255, black=True)
    image = models.FileField(upload_to='sharepage/ourImages', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}{self.created_at}'

    def get_absolute_url(self):
        return f'/{self.pk}/'

    def delete(self, *args, **kwargs):
        # 모델이 삭제될 때 연결된 파일도 함께 삭제
        if self.image:
            # 파일 삭제
            file_path = self.image.path
            # 썸네일 파일 삭제
            # file_t_path = f"{self.image.path.split('.')[0]}_t.{self.image.path.split('.')[1]}"
            # if os.path.exists(file_path) and os.path.exists(file_t_path):
            if os.path.exists(file_path):
                os.remove(file_path)
                # os.remove(file_t_path)
        super().delete(*args, **kwargs)

    # def download_image(self, id):
    #     if self.image:
    #         # 파일 다운로드
    #         file_path = self.image.path
    #         if os.path.exists(file_path):

    def get_t_url(self):
        return f"{self.image.url.split('.')[0]}_t.{self.image.url.split('.')[1]}"
