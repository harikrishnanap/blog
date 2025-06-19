from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
from blog.models import Post
from .forms import CustomUserCreationForm  # Adjust path as needed




# Create your views here.
from django.contrib import messages
from .models import Profile
from blog.models import Post  # if not already imported


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Create profile only if it doesn't already exist
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user)

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    recent_posts = Post.objects.order_by('-date_posted')[:3]

    context = {
        'form': form,
        'recent_posts': recent_posts
    }
    return render(request, 'users/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    recent_posts = Post.objects.order_by('-date_posted')[:3]

    context = {
        'form': form,
        'recent_posts': recent_posts
    }
    return render(request, 'users/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    if request.method =='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    recent_posts = Post.objects.order_by('-date_posted')[:3]
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'recent_posts': recent_posts,
        }

    return render(request, 'users/profile.html', context)
