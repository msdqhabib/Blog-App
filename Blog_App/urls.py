from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name= 'home'),
    path('user/<str:username>/', views.UserPostList.as_view(), name= 'user-posts'),
    path('<slug:slug>', views.PostDetail.as_view(), name= 'post_detail'),
    path('likes/<int:pk>', views.LikeView, name='like'),

]