import os
import json
from django.core.management.base import BaseCommand
from questions.models import Question
from openai import OpenAI

class Command(BaseCommand):
    help = 'Generates high-quality tech questions using OpenAI'

    def handle(self, *args, **kwargs):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = """
        Generate 5 advanced interview questions. 
        Format: JSON list of objects with "title", "category", "body", "answer".
        Categories must be: 'DJ' (Django), 'PY' (Python), or 'MA' (Math/Numpy).
        Focus on: Django 4.2 optimization, Python 3.12 features, and Linear Algebra for ML.
        """

        self.stdout.write("Calling OpenAI to generate questions...")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )

        # Parse the AI response
        raw_data = json.loads(response.choices[0].message.content)
        questions_list = raw_data.get('questions', [])

        for q in questions_list:
            Question.objects.get_or_create(
                title=q['title'],
                category=q['category'],
                body=q['body'],
                answer=q['answer']
            )
            self.stdout.write(self.style.SUCCESS(f"Added: {q['title']}"))