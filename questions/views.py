import requests
from django.shortcuts import render
from django.core.management import call_command
from django.views.decorators.http import require_POST
from .models import Question

# 1. The original list view for your homepage
def question_list(request):
    search_text = request.GET.get('search', '')
    questions = Question.objects.all()

    if search_text:
        questions = questions.filter(title__icontains=search_text)

    # Check if the request is coming from HTMX
    if request.headers.get('HX-Request'):
        return render(request, 'questions/partials/question_items.html', {'questions': questions})

    return render(request, 'questions/question_list.html', {'questions': questions})

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

@require_POST
def fetch_questions_view(request):
    print("🚀 Sync button was clicked!") # This will show in your terminal
    try:
        call_command('fetch_questions')
        print("✅ AI questions fetched successfully")
    except Exception as e:
        print(f"❌ Error during AI fetch: {e}")
        
    questions = Question.objects.all().order_by('-id') # Show newest first
    return render(request, 'questions/partials/question_items.html', {'questions': questions})