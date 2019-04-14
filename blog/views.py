from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# function view
def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': "just"
    }
    return render(request, "blog/home.html", context)

# class view
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts' # define the objects name so the home view still valid (unless use naming convention)
    ordering = ['-date_posted'] # add - sign to have newest at the top


class PostDetailView(DetailView):
    model = Post


def about(request):
    return render(request, "blog/about.html")
