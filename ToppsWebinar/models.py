from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import datetime

# Create your models here.

#Table of questions on the quiz
class Quiz1_Question(models.Model):
    question_text = models.CharField(max_length=350)
    def __str__(self):
        return self.question_text

#Table for the answers to each quiz question
class Quiz1_Answer(models.Model):
    question = models.ForeignKey(Quiz1_Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=300)
    correct_answer = models.BooleanField(default=False)
    def __str__(self):
        return self.answer_text


#Ties to the User model and keeps track of webinar progress
class Progress_Report(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    webinar_viewed = models.BooleanField(default=False)
    current_q1_question = models.IntegerField(default=1)
    quiz1_complete = models.BooleanField(default=False)
    quiz1_completion_date = models.DateField(null=True, blank=True)
    webinar_viewed.boolean = True
    quiz1_completion_date.short_description = 'Completion Date'
    def __str__(self):
        return self.user.username

"""
#Email new users to inform them of password
def email_new_user(sender, **kwargs):
    if kwargs["created"]:  # only for new users
        new_user = kwargs["instance"]
        m= 'Thank you for your interest in becoming a Certified Independent' \
           ' Installer. Completion of the webinar will entitle you to offer' \
           ' factory-backed warranties on qualifying jobs, and receive' \
           ' Certified Pricing on all purchases. \n \n ' \
           'Following is your log-in and password to log on to the Webinar. ' \
           'We recommend you have our manual available when you go through ' \
           'the webinar, as it comes in handy as a reference. \n ' \
           'Log on here: https://toppscertificationtest.azurewebsites.net \n ' \
           '\n Username: {0}

        send_mail(
            'Welcome to the Topps Products Certification Webinar',
            m,
            fail_silently=True,
        )
"""

#ties the Progress_Report model to the User model and auto-generate
# a new Progress Report when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Progress_Report.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.progress_report.save()

"""
*******************************************************************************
"""
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text