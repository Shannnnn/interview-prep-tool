import requests
from django.core.management.base import BaseCommand
from questions.models import Question

class Command(BaseCommand):
    help = 'Fetches tech questions from an online API'

    def handle(self, *args, **kwargs):
        # 1. The URL for Computer Science questions
        url = "https://opentdb.com/api.php?amount=10&category=18&type=multiple"
        
        self.stdout.write("Fetching data...")
        response = requests.get(url)
        data = response.json()

        if data['response_code'] == 0:
            for item in data['results']:
                # 2. Create the question in our Postgres DB
                Question.objects.get_or_create(
                    title=item['question'][:200], # Limit length
                    category="General Tech",
                    body=item['question'],
                    answer=item['correct_answer']
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported 10 questions!'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data.'))