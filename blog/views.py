from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import SearchForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
def home(request):
    posts_list = Post.objects.all().order_by('-date_posted')
    recent_post = posts_list[:3]
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        # 'posts': Post.objects.all()
        'page_obj' : page_obj,
        'recent_posts' : recent_post
    }
    return render(request, 'blog/home.html', context)


def about(request):
    recent_posts = Post.objects.order_by('-date_posted')[:3]

    return render(request, 'blog/about.html', {'recent_posts': recent_posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    recent_posts = Post.objects.order_by('-date_posted')[:3]
    context = {
        'post': post,
        'form' : form,
        'comments' : post.comments.all().order_by('-date_posted'),
        'recent_posts': recent_posts
    }
    return render(request, 'blog/post_detail.html', context)


#creating Post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-date_posted')[:3]
        return context


#updating Post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_message = "Post was updated successfully!"  # Add this line

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, self.success_message)  # Explicit message (optional)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-date_posted')[:3]
        return context


#deleting post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-date_posted')[:3]
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-date_posted')[:3]
        return context


def search(request):
    form = SearchForm()
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.filter(
                Q(title__icontains = query)|
                Q(content__icontains=query)|
                Q(author__username__icontains=query))
    recent_posts = Post.objects.order_by('-date_posted')[:3]

    return render(request, 'blog/search.html', {
        'form':form,
        'results':results,
        'query':request.GET.get('query',''),
        'recent_posts': recent_posts
    })


def category_posts(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(categories = category).order_by('-date_posted')
    paginator = Paginator(posts,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    recent_posts = Post.objects.order_by('-date_posted')[:3]


    context = {
        'category':category,
        'page_obj':page_obj,
        'recent_posts' : recent_posts
    }
    return render(request, 'blog/category_posts.html', context)