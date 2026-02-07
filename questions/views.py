import requests
from django.shortcuts import render
from .models import Question

# 1. The original list view for your homepage
def question_list(request):
    all_questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': all_questions})

# 2. The new FastAPI-powered challenge view
def daily_challenge(request):
    if request.method == "POST":
        user_answer = request.POST.get("user_answer")
        correct_answer = request.POST.get("correct_answer")
        
        is_correct = str(user_answer).strip() == str(correct_answer).strip()
        
        return render(request, 'questions/challenge_result.html', {
            'is_correct': is_correct,
            'correct_answer': correct_answer
        })

    # GET logic (fetch from FastAPI)
    response = requests.get("http://127.0.0.1:8000/generate/math", timeout=2)
    return render(request, 'questions/challenge.html', {'challenge': response.json()})