from django.shortcuts import render
from rest_framework import generics # rest 프레임워크의 제네릭 가져오기/ 제네릭뷰 사용할거니까
from .models import Post # Post 모델 가져오기
from .serializers import PostSerializer # PostSerializer 가져오기

# 제네릭 뷰 사용하는 이 부분은 http렌더링관련해서 찾아봐야할듯
class PostList(generics.ListAPIView):
    queryset = Post.objects.all() # 쿼리셋 설정해줘야하고
    serializer_class = PostSerializer # 시리얼라이저 클래스 설정해줘야함


