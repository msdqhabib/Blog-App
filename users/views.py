from django import forms
from django.db import models
from .forms import NewUserForm,ProfileForm,UserUpdateForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import  AuthenticationForm 
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def Register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration succesfull')
            return redirect('home')
        messages.error(request, 'Invalid Information')
    form = NewUserForm()
    context = {'register_form': form}
    return render(request, 'users/register.html', context )
    
def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, 'Congrats. You logged In! ')
                return redirect('home')
            else:
                messages.error(request, 'Incorrect Credentials!')
        else:
            messages.error(request, 'Invalid Information')
    
    form = AuthenticationForm()
    return render(request, 'users/login.html', context={'login_form': form})



def logout_view(request):
    logout(request)
    messages.info(request, 'You are succesfully Logged out')
    return redirect('home')

def Profile_page(request):
    user_form = NewUserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
                          
    context = {'user':request.user, 'user_form':user_form, 'profile_form': profile_form}
    return render(request, 'users/user.html', context)
    
@login_required
def Editprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST,
                             request.FILES,
                             instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            update_session_auth_hash(request, u_form)
            messages.success(request, f'Your account has been updated!')
            return redirect('profile-page')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/edit.html', context)        


def password_reset(request):
    return render(request, 'users/password_reset_form.html')
    