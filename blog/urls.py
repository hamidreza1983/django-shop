from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    path('category/<str:tag>', BlogView.as_view(), name='blog-category'),
    path('blog-details/<int:pk>',BlogDetataiView.as_view(), name='blog-details'),
    path('blogs/add_reply/<int:pk>',CreateReplayView.as_view(), name='add_reply'),
    path('blogs/add_comments/<int:pk>',CreateCommentView.as_view(), name='add_comment'),
]