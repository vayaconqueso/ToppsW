from django.contrib import admin
from .models import Quiz1_Question, Quiz1_Answer, Profile
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


"""
class ProfileInline(admin.StackedInline):
    model = Profile

class ExtendedUser(admin.ModelAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, ExtendedUser)
"""
admin.site.register(Quiz1_Question, QuestionAdmin)
admin.site.register(Profile)

