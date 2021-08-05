from django import template
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from authy.forms import SignUpForm, UpdateUserForm, UpdateProfileForm
from authy.models import Profile
from post.models import Follow, Post


def SignUpView(request):
    if request.method == "POST":

        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get('email')
            curr_user = User.objects.create_user(username=username, password=password, email=email)
            new_form = form.save(commit=False)
            new_form.user = curr_user
            new_form.save()
            return redirect('login')
    form = SignUpForm()
    return render(request, 'authy/Registration.html', {'form': form})


@login_required
def EditProfileView(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            email = user_form.cleaned_data.get('email')
            new_form = profile_form.save()
            new_form.email = email
            new_form.save()
            profile = Profile.objects.get(user__username=user_form.cleaned_data.get('username'))
            print(profile)
            return redirect('profile', user_id=profile.user.username)
    user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'authy/EditProfileForm.html', context)


@login_required
def ProfileView(request, user_id):
    user = get_object_or_404(User, username=user_id)
    profile = Profile.objects.get(user=user)
    followers = Follow.objects.filter(master=user)
    following = Follow.objects.filter(follower=user)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    context = {'profile': profile, 'followers': followers, 'following': following
        , 'posts': posts, }
    return render(request, 'authy/profile2.html', context)


class Search(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'authy/user_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        print(context)
        logged_in_user = self.request.user
        following = Follow.objects.filter(follower=logged_in_user)
        print(following)
        following_names = []
        for person in following:
            following_names.append(person.follower.username)
        for profile in context['object_list']:
            print(profile.user.username)
            person_name = profile.user.username
            if person_name in following_names:
                profile['following'] = True
        print(context)
        return context


@login_required
def SearchPage(request):
    all_users = Profile.objects.exclude(user=request.user)
    logged_in_user = request.user
    if request.method == 'GET':
        name = request.GET.get('username')
        print(name)
        if name:
            all_users = all_users.filter(user__username__istartswith=name)

    following = Follow.objects.filter(follower=logged_in_user)
    following_names = []
    for person in following:
        following_names.append(person.master.username)

    for user in all_users:
        username = user.user.username
        if username in following_names:
            user.following = True
        else:
            user.following = False
    for user in all_users:
        print(user.following)
    context = {
        'object_list': all_users,
    }
    return render(request, 'authy/user_list.html', context)
