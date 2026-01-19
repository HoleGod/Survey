from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Test, Answer, Question
import re

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
    if request.method == "POST":
        label = request.POST.get('label')
        banner = request.FILES.get('banner')
        test = Test.objects.create(author=request.user, title=label, image=banner)
        
        questions_nums = set()
        for key in request.POST.keys():
            m = re.match(r"question_(\d+)_text", key)
            if m:
                questions_nums.add(int(m.group(1)))
                
        for q_num in questions_nums:
            text = request.POST.get(f'question_{q_num}_text')
            type = request.POST.get(f'question_{q_num}_type')
            
            question = Question.objects.create(
                test=test,
                text=text,
                question_type=type,
            )
            
            a_num = 1
            answers_dict = {}
            
            while f"question_{q_num}_answer_{a_num}" in request.POST:
                text_a = request.POST.get(f"question_{q_num}_answer_{a_num}")
                answer = Answer.objects.create(
                    question=question,
                    text=text_a,
                )
                answers_dict[a_num] = answer
                a_num += 1
            
            if question.question_type == "single":
                correct = request.POST.get(f'question_{q_num}_correct')
                if correct:
                    answers_dict[int(correct)].is_correct = True
                    answers_dict[int(correct)].save()
                    
            else:
                for c in request.POST.getlist(f"question_{q_num}_correct"):
                    answers_dict[int(c)].is_correct = True
                    answers_dict[int(c)].save()
        
    return redirect("index")
    
@login_required
def create_test_page(request):
    return render(request, "testing/test_creator.html")
    