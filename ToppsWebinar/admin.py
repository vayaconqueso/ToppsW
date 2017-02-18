from django.contrib import admin
from .models import Quiz1_Question, Quiz1_Answer
# Register your models here.


class AnswerInline(admin.TabularInline):
    model = Quiz1_Answer
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['question_text']}),
    ]
    inlines = [AnswerInline]
    list_display = ['question_text']
    search_fields = ['question_text']


admin.site.register(Quiz1_Question, QuestionAdmin)
