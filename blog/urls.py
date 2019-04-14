from django.urls import path, include
from . import views
from .views import PostListView, PostDetailView

app_name = "blog"

urlpatterns =[
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]

# looking for a template: <app>/<model>_<viewtype>.html => blog/post_list.html