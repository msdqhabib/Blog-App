from cProfile import Profile
import imp
from typing import ContextManager
from unittest import result
from django.db import models
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import  AuthenticationForm
from django.views import generic
from setuptools import Require
from .models import STATUS, Post
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.models import User




class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'Blog_App/index.html'

class UserPostList(generic.ListView):
    model = Post
    template_name = 'Blog_App/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created_on')
        



class PostDetail(generic.DetailView):
    model = Post
    template_name = 'Blog_App/post_detail.html'
     

    
def LikeView(request, pk):
    user = request.user
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if not user.is_authenticated:
        messages.info(request, 'You need to login for using Like option')
        return redirect(request.META['HTTP_REFERER'],'home')
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    context = {
        'post':post,
        'liked':liked,
        'total_likes':post.likes.count(),
    }
    return redirect(request.META['HTTP_REFERER'],'home')
