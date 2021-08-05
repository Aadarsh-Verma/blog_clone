from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

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


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-date_posted']
    template_name = 'post/user_post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        followers = Follow.objects.filter(follower=user)
        followers_name = []
        for follower in followers:
            followers_name.append(follower.master.username)

        posts = []
        for post in context['object_list']:
            if post.author.username in followers_name:
                posts.append(post)

        context['posts'] = posts
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        print(post)
        print(request.POST)
        if request.method == "POST":
            form = CommentCreationForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.author = request.user
                new_form.post = post
                new_form.save()
                return redirect(reverse('post_detail', kwargs={'pk': post.id}))

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
        print(context)
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
@csrf_exempt
def LikeView(request):
    print("request is ")
    print(request.POST)
    if request.method == 'POST':
        pk = int(request.POST['pk'])
        print("pk is " + str(pk))
        post = get_object_or_404(Post, pk=pk)
        temp = post.likes
        if not Like.objects.filter(post=post, user=request.user).exists():
            post.likes = post.likes + 1
            post.save()
            temp = post.likes
            Like.objects.get_or_create(post=post, user=request.user)

        print("temp is " + str(temp))
        return JsonResponse({'like': temp})
    return JsonResponse({'like': str(request)})


@login_required
def follow(request, pk):
    print("follow called")
    master = User.objects.get(id=pk)
    follower = request.user
    if master != follower:
        Follow.objects.get_or_create(master=master, follower=follower)
    return redirect('search')


@login_required
def unfollow(request, pk):
    print("unfollow called")
    master = User.objects.get(id=pk)
    follower = request.user
    print(str(master.username) + " " + str(follower.username))
    if master != follower:
        obj = get_object_or_404(Follow, master=master, follower=follower)
        obj.delete()
    return redirect('search')


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'post/post_detail.html'
    context_object_name = 'comments'
    ordering = ['-date_posted']


def CommentCreateView(request, pk):
    print(request.POST)
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
