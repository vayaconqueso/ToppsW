from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Choice, Question, Quiz1_Answer, Quiz1_Question, Profile

"""
class IndexView(generic.ListView):
    template_name = 'ToppsWebinar/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
"""

def index(request):
    return render(request, 'ToppsWebinar/index.html')

def landing(request):
    current_user = request.user
    profile = Profile.objects.get(user_id=current_user)
    current_question = profile.current_q1_question
    return render(request, 'ToppsWebinar/landing.html', {'current_question': current_question})

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

def quiz1_question(request, question_id):
    question = get_object_or_404(Quiz1_Question, pk=question_id)
    return render(request, 'ToppsWebinar/q1.html', {'question': question})