from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Test, Answer, Question, UserTest, UserAnswer
import re
from .utils import compare_data
from typing import List
from .services.exel_export import export_exel

@login_required
def runtest(request, id: int):
    test = Test.objects.get(id=id)
    questions = test.questions.prefetch_related("answers")

    return render(
        request,
        "testing/test_page.html",
        {
            "test": test,
            "questions": questions,
        },
    )

@login_required
def sent_test(request):
    print(request.POST)
    
    test_id = request.POST.get('test_id')
    test = Test.objects.get(id=test_id)
    user_test = UserTest.objects.create(test=test, user=request.user)
    
    q_ids = request.POST.getlist("q_id")
    total: int = 0
    
    answer_dict: dict[str, List[str]] = {}
    for q_id in q_ids:
        question = Question.objects.get(id=q_id)
        user_answer = UserAnswer.objects.create(question=question, user_test=user_test)
        
        correct_dict = {}
        correct_dict[q_id] = list(
            map(str, question.answers.filter(is_correct=True).values_list('id', flat=True))
        )
        answer_ids = request.POST.getlist(f"question_{q_id}")
        
        user_answer.selected_answers.set(answer_ids)
        answer_dict[q_id] = answer_ids
        
        itn = compare_data(correct_dict, answer_dict)
        total = len(itn)
        
    context = {
        "user_answers": answer_dict,
        "test": test,
        "questions":  test.questions.all(),
        "user_test": user_test,
        "total": total,
    }
    
    print(context)
    
    return render(
        request,
        "testing/test_result.html",
        context=context,
    )
    
@login_required
def create_test(request):
    print(request.POST)
    if request.method == "POST":
        label = request.POST.get("label")
        banner = request.FILES.get("banner")
        test = Test.objects.create(author=request.user, title=label, image=banner)

        questions_nums = set()
        for key in request.POST.keys():
            m = re.match(r"question_(\d+)_text", key)
            if m:
                questions_nums.add(int(m.group(1)))

        for q_num in questions_nums:
            text = request.POST.get(f"question_{q_num}_text")
            type = request.POST.get(f"question_{q_num}_type")

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
                correct = request.POST.get(f"question_{q_num}_correct")
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

@login_required
def get_file_exel(request, test_id: int):
    test = Test.objects.get(id=test_id)
    
    file_path = export_exel(test=test)
    
    if not file_path:
        raise Http404("File not found")
    
    return FileResponse(
		open(file_path, "rb"),
		as_attachment=True,
		filename=file_path.name
	)