from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Quiz1_Question, Quiz1_Answer, Progress_Report
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


class PRAdmin(admin.ModelAdmin):
    model = Progress_Report
    list_display = ['user', 'webinar_viewed', 'quiz1_completion_date']

UserAdmin.list_display = ('username', 'first_name', 'last_name')
"""
class ProfileInline(admin.StackedInline):
    model = Progress_Report


class ExtendedUser(admin.ModelAdmin):
    inlines = [ProfileInline]
    list_display = ('username', 'first_name', 'last_name')
"""
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Quiz1_Question, QuestionAdmin)
admin.site.register(Progress_Report, PRAdmin)
