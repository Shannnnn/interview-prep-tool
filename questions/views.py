import requests
from django.shortcuts import render
from .models import Question

# 1. The original list view for your homepage
def question_list(request):
    all_questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': all_questions})

# 2. The new FastAPI-powered challenge view
def daily_challenge(request):
    try:
        # Note: Ensure FastAPI is running on port 8000
        response = requests.get("http://127.0.0.1:8000/generate/math", timeout=2)
        api_data = response.json()
    except Exception:
        api_data = {
            "title": "Service Offline",
            "body": "Could not connect to the FastAPI Math Generator.",
            "answer": "N/A"
        }
    return render(request, 'questions/challenge.html', {'challenge': api_data})