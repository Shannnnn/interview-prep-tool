from django.contrib import admin
from .models import Question

# This tells Django: "Show the Question table in the Admin panel"
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category') # Show these columns in the list view
    list_filter = ('category',)          # Add a sidebar to filter by category