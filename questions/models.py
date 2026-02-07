from django.db import models

class Question(models.Model):
    STACK_CHOICES = [
        ('PY', 'Python'),
        ('DJ', 'Django'),
        ('MA', 'Math/Numpy'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=STACK_CHOICES)
    body = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"