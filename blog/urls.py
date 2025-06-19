from django.urls import path
from . import views
from .views import PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, category_posts

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('search/', views.search, name='search'),
    path('category/<str:category_name>/', views.category_posts, name='category-posts'),
]