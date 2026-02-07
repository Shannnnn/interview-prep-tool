from django.shortcuts import render
from .models import Question

def question_list(request):
    # 1. Fetch all questions from the database
    all_questions = Question.objects.all()
    
    # 2. Package them into a 'context' dictionary
    context = {
        'questions': all_questions
    }
    
    # 3. Send the data to the HTML template
    return render(request, 'questions/question_list.html', context)