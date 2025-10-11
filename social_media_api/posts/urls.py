from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, LikePostView, UnlikePostView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]


from django.urls import path
from .views import FeedView

urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    ]
    
   
