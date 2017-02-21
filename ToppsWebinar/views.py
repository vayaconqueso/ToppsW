from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail


from .models import Choice, Question, \
    Quiz1_Answer, Quiz1_Question, Progress_Report


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


def wbwatched(request):
    current_user = request.user
    user = User.objects.get(username=current_user)
    user.progress_report.webinar_viewed = True
    user.save()
    return redirect('/ToppsWebinar/landing')


def quiz1_controller(request, question_id):
    # check for completion of the Webinar
    max_questions = Quiz1_Question.objects.count()
    current_user = request.user
    user = User.objects.get(username=current_user)
    if user.progress_report.current_q1_question > max_questions:
        if user.progress_report.quiz1_complete == False:
            # send email notification of completion
            send_mail(
                'Certification Webinar complete!',
                '{0} has completed the webinar.'.format(
                    user.first_name + user.last_name),
                'toppscert@toppsproducts.com',
                ['dwarner@cenetric.com'],
                fail_silently=True,
            )
            # update the model to record completion status
            user.progress_report.quiz1_complete = True
            user.progress_report.quiz1_completion_date = timezone.now()
            user.save()
        return render(request, 'ToppsWebinar/q1complete.html')
    # prevent users from skipping around in the quiz
    elif int(question_id) != int(user.progress_report.current_q1_question):
        return HttpResponse('Unauthorized', status=403)
    # continue to the next question
    else:
        question = get_object_or_404(Quiz1_Question, pk=question_id)
        return render(request, 'ToppsWebinar/q1.html', {'question': question})


def quiz1_answer(request, question_id):
    question = get_object_or_404(Quiz1_Question, pk=question_id)
    try:
        selected_choice = \
            question.quiz1_answer_set.get(pk=request.POST['answer'])
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
            return HttpResponseRedirect(reverse(
                'ToppsWebinar:quiz1_question', args=(question.id + 1,)))
        else:
            return render(request, 'ToppsWebinar/q1.html', {
                'question': question,
                'error_message': "I'm sorry, that is incorrect. Please try again.",
            })

