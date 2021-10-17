from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/create/', views.create_user),
    path('posts/create/', views.create_post),

    path('users/top/', views.top_users_list),
    path('users/follow/', views.follow),
    path('users/feed/<int:pk>/', views.feed),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),

    ]
