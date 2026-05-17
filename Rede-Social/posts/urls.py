from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('publicar/', views.post_create, name='post_create'),
    path('publicacao/<int:pk>/eliminar/', views.post_delete, name='post_delete'),
    path('publicacao/<int:pk>/like/', views.post_like, name='post_like'),
    path('publicacao/<int:pk>/comentar/', views.post_comment, name='post_comment'),
    path('utilizador/<str:username>/', views.user_posts, name='user_posts'),
]
