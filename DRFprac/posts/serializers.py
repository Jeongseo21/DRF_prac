from rest_framework import serializers
# 시리얼라이저 가져오고
from .models import Post # Post 모델 가져오기

# 모델을 가져와서 직렬화하겠다는거, 매개변수 모델 시리얼라이저
class PostSerializer(serializers.ModelSerializer):
    # 게시자는 변경할 수 없도록 
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')

    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'poster','poster_id', 'created'] # 포스트 모델에서 가져올 필드 정하기 id는 자동생성


