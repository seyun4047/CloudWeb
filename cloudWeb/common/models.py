from django.db import models
from django.utils import timezone

class AuthenticationKey(models.Model):
    key = models.CharField(max_length=100, unique=True)  # 유니크한 인증키
    is_valid = models.BooleanField(default=True)  # 인증키의 유효 여부
    # created_at = models.DateTimeField(default=timezone.now)  # 인증키 생성일시
    # class Meta:
    #     db_table = 'user_auth_key'
    def __str__(self):
        return self.key