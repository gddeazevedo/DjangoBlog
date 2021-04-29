from django.shortcuts import render
from .models import Post


def home(request):
    '''Handles the traffic of the home page'''
    posts = Post.objects.all()

    context = {'posts': posts}
    return render(request, 'blogs/home.html', context)


def about(request):
    context = {'title': 'About'}
    return render(request, 'blogs/about.html', context)
