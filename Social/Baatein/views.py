from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import Profile, Talk
from django.contrib.auth.models import User
from .forms import TalkForm, SignUpForm, UserUpdateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def home(request):
    return render(request, 'home.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(
                request, ("Invalid Username or Password .."))
            return redirect('home')

    else:
        return render(request, 'home.html')


def logout_user(request):
    logout(request)
    messages.success(
        request, ("Thank You For Visiting.."))
    return render(request, 'home.html')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def index(request):
    if request.user.is_authenticated:
        form = TalkForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                talk = form.save(commit=False)
                talk.user = request.user
                talk.save()
                return redirect('index')

        talks = Talk.objects.all().order_by("-created_at")
        return render(request, 'index.html', {"talks": talks, "form": form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return render(request, 'home.html')


def members(request):
    if request.user.is_authenticated:
        member_list = Profile.objects.exclude(user=request.user)
        return render(request, 'members.html', {"member_list": member_list})
    else:
        response = HttpResponseRedirect('/')
        response.status_code = 403
        return response
        # messages.success(request, "You Must Be Logged In...")
        # return render(request, 'home.html')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        talks = Talk.objects.filter(user_id=pk)
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST.get('follow')
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, 'profile.html', {"profile": profile, "talks": talks})
    else:
        response = HttpResponseRedirect('/')
        response.status_code = 403
        return response
        # messages.success(request, "You Must Be Logged In...")
        # return render(request, 'home.html')


@login_required
def update_user(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if 'update_profile' in request.POST and user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('index')
        elif 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            # Important to keep the user logged in
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully.")
            return redirect('index')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'update_user.html', {
        'user_form': user_form,
        'password_form': password_form
    })


def talk_show(request, pk):
    talk = get_object_or_404(Talk, id=pk)
    comments = talk.comments.all()
    comment_form = CommentForm()
    return render(request, "show.html", {
        'talk': talk,
        'comments': comments,
        'comment_form': comment_form
    })


def comment_talk(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    talk = get_object_or_404(Talk, id=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.talk = talk
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment has been added!")
            return redirect('index')
        else:
            print(form.errors)
            messages.error(
                request, "Error posting your comment. Please check your input.")
            return redirect('index')

    return redirect('index')
