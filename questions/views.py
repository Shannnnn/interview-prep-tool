import requests
from django.shortcuts import render
from .models import Question

def daily_challenge(request):
    # 1. Ask FastAPI for a fresh math problem
    try:
        response = requests.get("http://127.0.0.1:8000/generate/math", timeout=2)
        api_data = response.json()
    except:
        # Fallback if FastAPI server is down
        api_data = {
            "title": "Error",
            "body": "Could not connect to the Math Service.",
            "answer": "N/A"
        }

    return render(request, 'questions/challenge.html', {'challenge': api_data})