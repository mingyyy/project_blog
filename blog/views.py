from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Event
from datetime import datetime, date, timedelta
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.safestring import mark_safe
from .utils import Calendar
import calendar
from .forms import EventForm, ContactForm, EventDeleteForm
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from django.contrib import messages



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


class CalendarView(ListView):
    model = Event
    template_name = 'blog/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def prev_month(m):
    first = m.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(m):
    days_in_month = calendar.monthrange(m.year, m.month)[1]
    last = m.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_date(req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
        return datetime.today()


@login_required
def event(request, event_id=None):
    instance = Event()

    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    form_confirm = EventDeleteForm(request.POST or None)

    if request.POST and form.is_valid():
        event = form.save(commit=False)
        if event.event_duration() is False:
            messages.warning(request, "Your start and end dates are not valid!")
            return redirect('blog:calendar')
        event.author = request.user
        event.save()
        try:
            if request.POST['confirm'] == 'confirm':
                event.delete()
                messages.warning(request, "The event has been deleted!")
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('blog:calendar'))
    context = {'form': form, "pk": event_id, 'form_confirm': form_confirm}
    return render(request, 'blog/event.html',context)


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            message = Mail(
                from_email=form.cleaned_data['from_email'],
                # to_emails=form.cleaned_data['to_email'],
                to_emails="j.yanming@gmail.com",
                subject=form.cleaned_data['subject'],
                html_content=form.cleaned_data['content'],)
            try:
                # send_mail(subject, message, from_email, ['j.yanming@gmail.com'])
                sg = SendGridAPIClient(os.environ.get('API_KEY'))
                response = sg.send(message)
                messages.success(request, "Your message has been sent! Thank you for contacting us.")
                print(response.status_code)
            except BadHeaderError as e:
                return HttpResponse(e.message)
            return redirect('blog:blog-home')
    return render(request, "blog/contact.html", {'form': form})


# def search(request):
#     template = "blog/search.html"
#     query = request.GET.get('q')
#
#     if query:
#         posts = PostDocument.search().query('match', title=query)
#     else:
#         posts = ''
#     return render(request, template, {'posts':posts})

# @api_view(['POST'])
# def search_post(request):
#     title = request.data['title']
#     posts = SearchQuerySet().models(Post).autocomplete(
#         title__startswith=title)
#
#     searched_data = []
#     for i in posts:
#         all_results = {"title": i.title,
#                        "content": i.content,
#                        }
#         searched_data.append(all_results)
#
#     return Response(searched_data)




