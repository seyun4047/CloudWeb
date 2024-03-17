from django.db import models
import os
# Create your models here.

# FilmGen
class Post(models.Model): # filmPost
    # title = models.CharField(max_length=255, black=True)
    image = models.FileField(upload_to='lab/film/images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}{self.created_at}'

    def get_absolute_url(self):
        return f'/{self.pk}/'

    def get_img_src(self):
        if self.image:
            return self.image.url

    def delete(self, *args, **kwargs):
        # 모델이 삭제될 때 연결된 파일도 함께 삭제
        if self.image:
            # 파일 삭제
            file_path = self.image.path
            if os.path.exists(file_path):
                os.remove(file_path)
        super().delete(*args, **kwargs)

 # ImgStacker Upload
class ImgStackerPost(models.Model):
    # title = models.CharField(max_length=255, black=True)
    image = models.FileField(upload_to='lab/ImgStacker/images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}{self.created_at}'

    def get_absolute_url(self):
        return f'/{self.pk}/'

    def get_img_src(self):
        if self.image:
            return self.image.url

    def delete(self, *args, **kwargs):
        # 모델이 삭제될 때 연결된 파일도 함께 삭제
        if self.image:
            # 파일 삭제
            file_path = self.image.path
            if os.path.exists(file_path):
                os.remove(file_path)
        super().delete(*args, **kwargs)


class QRPost(models.Model):
    # title = models.CharField(max_length=255, black=True)
    image = models.FileField(upload_to='lab/QR/images', blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}{self.created_at}'

    def get_absolute_url(self):
        return f'/{self.pk}/'

    def get_img_src(self):
        if self.image:
            return self.image.url

    def delete(self, *args, **kwargs):
        # 모델이 삭제될 때 연결된 파일도 함께 삭제
        if self.image:
            # 파일 삭제
            file_path = self.image.path
            if os.path.exists(file_path):
                os.remove(file_path)
        super().delete(*args, **kwargs)