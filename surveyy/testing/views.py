from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Test

def index(request):
    return render(request, "testing/home.html")

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = UserLoginForm()
    return render(request, "testing/login.html", {"form": form})

def signin(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SignIn is success!")
            return redirect("login")
        else:
            messages.error(request, "SignIn is failed!")
    else:
        form = UserRegisterForm()
    return render(request, "testing/register.html", {"form": form})

@login_required
def user_logout(request):
	logout(request)
	return redirect("index")

@login_required
def profile(request):
    user = request.user
    surveys = Test.objects.filter(author=user).all()
    return render(request, "testing/profile.html", {"user": user, "surveys": surveys})

@login_required
def runtest(request):
    ...
    
@login_required
def create_test(request):
    ...
    