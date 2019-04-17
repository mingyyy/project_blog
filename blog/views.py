from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
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
    paginate_by = 5 # 2 posts per page


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts' # define the objects name so the home view still valid (unless use naming convention)
    # ordering = ['-date_posted'] # add - sign to have newest at the top
    paginate_by = 5 # 2 posts per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin,CreateView):
    # instead of decorator we have to use LoginRequiredMixin
    model = Post
    fields = ['title','content'] # date_created and author will be filled automatically

    def form_valid(self, form):
        # overwrite the form_valid method
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # instead of decorator we have to use LoginRequiredMixin
    # make sure the author is the current login user => UserPassesTestMixin
    model = Post
    fields = ['title','content'] # date_created and author will be filled automatically

    def form_valid(self, form):
        # overwrite the form_valid method
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html")
