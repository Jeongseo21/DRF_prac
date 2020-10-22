from django.db import models
from django.contrib.auth.models import User

# db테이블 만들기
class Post(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    # 포스터는 유저를 상속받는다(외래키 활용, 유저와 1대 다 관계)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)