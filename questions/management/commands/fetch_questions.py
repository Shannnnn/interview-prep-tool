import os
import json
from groq import Groq
from google import genai
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from questions.models import Question
from openai import OpenAI

load_dotenv()

# class Command(BaseCommand):
#     help = 'Generates high-quality tech questions using OpenAI'

#     def handle(self, *args, **kwargs):
#         client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#         prompt = """
#         Generate 5 advanced interview questions. 
#         Format: JSON list of objects with "title", "category", "body", "answer".
#         Categories must be: 'DJ' (Django), 'PY' (Python), or 'MA' (Math/Numpy).
#         Focus on: Django 4.2 optimization, Python 3.12 features, and Linear Algebra for ML.
#         """

#         self.stdout.write("Calling OpenAI to generate questions...")
        
#         response = client.chat.completions.create(
#             model="gpt-4o",
#             messages=[{"role": "user", "content": prompt}],
#             response_format={ "type": "json_object" }
#         )

#         # Parse the AI response
#         raw_data = json.loads(response.choices[0].message.content)
#         questions_list = raw_data.get('questions', [])

#         for q in questions_list:
#             Question.objects.get_or_create(
#                 title=q['title'],
#                 category=q['category'],
#                 body=q['body'],
#                 answer=q['answer']
#             )
#             self.stdout.write(self.style.SUCCESS(f"Added: {q['title']}"))

# class Command(BaseCommand):
#     help = 'Generates tech questions using the 2026 standard Gemini 2.0 model'

#     def handle(self, *args, **kwargs):
#         # The new SDK automatically handles the versioning (v1) 
#         # when you use the Client() constructor correctly.
#         client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
#         # 2026 Standard Model Name (no 'models/' prefix needed for this SDK)
#         target_model = 'gemini-2.0-flash' 
        
#         prompt = """
#         Generate 5 tech interview questions in JSON.
#         Format: {"questions": [{"title": "...", "category": "DJ", "body": "...", "answer": "..."}]}
#         Categories: DJ (Django), PY (Python), MA (Math/Numpy).
#         Return ONLY the raw JSON.
#         """

#         self.stdout.write(f"🚀 Using {target_model} to generate questions...")
        
#         try:
#             response = client.models.generate_content(
#                 model=target_model,
#                 contents=prompt
#             )
            
#             # The .text property is the cleanest way to get the response
#             raw_text = response.text.strip()
            
#             # Some safety cleaning if the AI adds markdown blocks
#             if raw_text.startswith("```json"):
#                 raw_text = raw_text.replace("```json", "").replace("```", "").strip()
            
#             data = json.loads(raw_text)
            
#             for q in data.get('questions', []):
#                 Question.objects.get_or_create(
#                     title=q['title'],
#                     category=q['category'],
#                     body=q['body'],
#                     answer=q['answer']
#                 )
#                 self.stdout.write(self.style.SUCCESS(f"✅ Added: {q['title']}"))

#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
#             self.stdout.write("Note: If 404 persists, try model 'gemini-2.0-flash-lite' or 'gemini-pro'")

class Command(BaseCommand):
    help = 'Fetches questions using Groq (Llama 3) for free'

    def handle(self, *args, **kwargs):
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        prompt = """
        Generate 5 advanced tech interview questions in JSON format.
        Format: {"questions": [{"title": "...", "category": "DJ", "body": "...", "answer": "..."}]}
        Categories: DJ (Django), PY (Python), MA (Math/Numpy).
        Return ONLY the JSON.
        """

        self.stdout.write("🚀 Calling Groq (Llama 3)...")
        
        try:
            chat_completion = client.chat.completions.create(
                # Llama 3 is incredibly fast and smart for this
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                response_format={"type": "json_object"} # Forces valid JSON
            )

            raw_text = chat_completion.choices[0].message.content
            data = json.loads(raw_text)
            
            for q in data.get('questions', []):
                Question.objects.get_or_create(
                    title=q['title'],
                    category=q['category'],
                    body=q['body'],
                    answer=q['answer']
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Added: {q['title']}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Groq Error: {e}"))