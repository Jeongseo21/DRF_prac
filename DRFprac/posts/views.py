from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status # rest 프레임워크의 제네릭 가져오기/ 제네릭뷰 사용할거니까
from rest_framework.exceptions import ValidationError #exceptions 가져오기
from rest_framework.response import Response # delete할 때 필요한 리스폰스 가져오기
# permissions 가져와서 권한있는 사용자 구분
from .models import Post, Vote # Post 모델 가져오기
from .serializers import PostSerializer, VoteSerializer # PostSerializer 가져오기

# 제네릭 뷰 사용하는 이 부분은 http렌더링 관련해서 찾아봐야할듯
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all() # 쿼리셋 설정해줘야하고
    serializer_class = PostSerializer # 시리얼라이저 클래스 설정해줘야함

    # 권한있는지 확인하는 permission_class(로그아웃 상태로는 list볼 수 있지만 create는 불가능)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # create 이벤트를 만들 때마다 poster를 만들거야
        serializer.save(poster=self.request.user)

class PostRestrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all() # 쿼리셋 설정해줘야하고
    serializer_class = PostSerializer # 시리얼라이저 클래스 설정해줘야함

    # 권한있는지 확인하는 permission_class(로그아웃 상태로는 list볼 수 있지만 create는 불가능)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 로그인한 사용자가 post 게시자와 다르면 삭제하지 못하게 하는 메서드
    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This isn\'t your post to delete!')
class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin): # list필요없고 create만 하면 되니까, mixin은 delete때문에 가져온거
    serializer_class = VoteSerializer # 시리얼라이저 클래스 설정해줘야함

    # 권한있는지 확인하는 permission_class(로그아웃 상태로는 create할 수 없음)
    permission_classes = [permissions.IsAuthenticated]

    # user와 post를 여기서 만들어주겠다는거
    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk']) # url에서 받아오는 int:pk를 가져와서 pk에 넣는다
        return Vote.objects.filter(voter=user, post=post) # 가져온 user와 post를 Vote의 쿼리셋으로 설정
    
    # class마다 perform_create 매서드를 만들어야 create가 제대로 된다.
    def perform_create(self, serializer):
        # 이미 get_queryset()이 실행됐다면 이미 vote를 한 거니까 ValidationError 발생시키기
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post!')
        # create 이벤트를 만들 때마다 voter랑 post를 만들거야
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))
    
    #vote한 게시물을 취소하고 싶을 때 (url주소에 <int:pk>가 있기 때문에 가능)
    def delete(self, request, *args, **kwargs):
        # 만약 get_queryset이 존재하면 queryset을 delete하고 http204 리턴해주기
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never voted for this post!')