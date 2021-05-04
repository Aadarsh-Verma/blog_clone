from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from post.forms import CommentCreationForm
from post.models import Post, Like, Follow, Comment


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-date_posted']
    template_name = 'post/post_list.html'


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def post(self, request,*args,**kwargs):
        post = self.get_object()

        if request.method == "POST":
            form = CommentCreationForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.author = request.user
                new_form.post = post
                new_form.save()
                return redirect(reverse('post_detail',kwargs={'pk':post.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        like = Like.objects.filter(post=post)
        comments = Comment.objects.filter(post=post).order_by('-date_posted')
        # Comment Creation View

        form = CommentCreationForm()

        context["form"] = form
        context["comments"] = comments
        context["likes"] = like
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['picture', 'caption']
    template_name = 'post/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['picture', 'caption']
    template_name = 'post/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes = post.likes + 1
    post.save()
    Like.objects.get_or_create(post=post, user=request.user)
    return redirect('post_list')


@login_required
def follow(request, pk):
    master = User.objects.get(id=pk)
    follower = request.user
    if master != follower:
        Follow.objects.get_or_create(master=master, follower=follower)
    return redirect('search')


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'post/post_detail.html'
    context_object_name = 'comments'
    ordering = ['-date_posted']


def CommentCreateView(request, pk):
    if request.method == "POST":
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.author = request.user
            new_form.post = Post.objects.get(id=pk)
            new_form.save()
            return redirect(reverse('post_detail', kwargs={'pk': pk}))
    form = CommentCreationForm()
    return render(request, 'post/comment_create.html', {'form': form})
