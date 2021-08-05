from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from post.views import PostUpdateView, PostCreateView, PostDeleteView, PostListView, PostDetailView, LikeView, follow, \
    CommentCreateView, UserPostListView, unfollow

urlpatterns = [
    path('post_update/<pk>', PostUpdateView.as_view(), name='post_update'),
    path('post_detail/<pk>', PostDetailView.as_view(), name='post_detail'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('post_list/', PostListView.as_view(), name='post_list'),
    path('user_post_list/', UserPostListView.as_view(), name='user_post_list'),
    path('post_delete/<pk>', PostDeleteView.as_view(), name='post_delete'),
    path('post_like/', LikeView, name='like'),
    path('user_follow/<pk>', follow, name='follow'),
    path('user_unfollow/<pk>', unfollow, name='unfollow'),
    # path('comment_create/<pk>', CommentCreateView, name='comment_create'),
]
