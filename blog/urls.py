from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    # Posts
    path('post/novo_post', views.novo_post, name='novo_post'),
    path('post/<int:post_id>/post_detail', views.post_detail, name='post_detail'),
    #
    path('user/login/', views.login, name="login"),
    path('user/register/', views.register, name="register")
]