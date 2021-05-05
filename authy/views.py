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
            Profile.objects.get(user__username=user_form.cleaned_data.get('username')).refresh_from_db()
            print(Profile.objects.get(user__username=user_form.cleaned_data.get('username')))
            return redirect('login')
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
