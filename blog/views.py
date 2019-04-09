from django.shortcuts import render
from django.http import HttpResponse

posts=[
    {
    'author': "Ming",
    'title': "Blog Post 1",
    'content': 'welcome to bali',
    'date_posted': 'August 27, 2018'
    },
    {
        'author': "Martin",
        'title': "Blog Post 2",
        'content': 'exam time, are you ready',
        'date_posted': 'August 27, 2019'

    }]


def home(request):
    context={
        'posts':posts,
        'title': "just"
    }
    return render(request, "blog/home.html", context)

def about(request):
    return render(request, "blog/about.html")