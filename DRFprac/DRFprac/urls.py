from django.contrib import admin
from django.urls import path, include
from posts import views # posts앱의 views파일 가져오겠다

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/posts', views.PostList.as_view()), # views.py의 클래스를 그대로 가져오면 됨
    path('api/posts/<int:pk>', views.PostRestrieveDestroy.as_view()),
    path('api/posts/<int:pk>/vote', views.VoteCreate.as_view()),
    path('api-auth/', include('rest_framework.urls')), # test page에서 로그인/로그아웃 가능하게 해주는거
]
