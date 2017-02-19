from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Choice, Question, Quiz1_Answer, Quiz1_Question, Progress_Report


def index(request):
    return render(request, 'ToppsWebinar/index.html')


def landing(request):
    profile = Progress_Report.objects.get(user_id=request.user)
    current_question = profile.current_q1_question
    watched_status = profile.webinar_viewed
    return render(request, 'ToppsWebinar/landing.html', {
        'current_question': current_question, 'watched_status': watched_status})


def webinar(request):
    return render(request, 'ToppsWebinar/webinar.html')


def quiz1_question(request, question_id):
    question = get_object_or_404(Quiz1_Question, pk=question_id)
    return render(request, 'ToppsWebinar/q1.html', {'question': question})


def quiz1_answer(request, question_id):
    question = get_object_or_404(Quiz1_Question, pk=question_id)
    try:
        selected_choice = question.quiz1_answer_set.get(pk=request.POST['answer'])
    except (KeyError, Quiz1_Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'ToppsWebinar/q1.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if (selected_choice.correct_answer):
            current_user = request.user
            user = User.objects.get(username=current_user)
            user.progress_report.current_q1_question += 1
            user.save()
            return HttpResponseRedirect(reverse('ToppsWebinar:quiz1_question', args=(question.id +1,)))
        else:
            return render(request, 'ToppsWebinar/q1.html', {
                'question': question,
                'error_message': "I'm sorry, that is incorrect. Please try again.",
            })

"""
***********************************************************************************************************************
"""
class DetailView(generic.DetailView):
    model = Question
    template_name = "ToppsWebinar/detail.html"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "ToppsWebinar/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form.
        return render(request, 'ToppsWebinar/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('ToppsWebinar:results', args=(question.id,)))