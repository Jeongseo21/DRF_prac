from django.contrib import admin
from .models import Post, Vote # 모델 만든거 가져오기

admin.site.register(Post)
admin.site.register(Vote)