from django.db import models
from django.utils import timezone
import datetime

from users.models import InstructorAccount, StudentAccount






class Quiz(models.Model):
    DIFFICULT_CHOICES = [
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('hard', 'hard'),
    ]
    schedule_name 		   = models.CharField(max_length=50)
    user                   = models.ForeignKey(InstructorAccount, on_delete=models.CASCADE)
    company_name           = models.CharField(max_length=50)
    name                   = models.CharField(max_length=50, unique=True)
    quiz_code              = models.CharField(max_length=50, unique=True)
    topic                  = models.CharField(max_length=50)
    number_of_chosen_questions = models.IntegerField()
    number_of_theory_questions = models.IntegerField()
    time                   = models.IntegerField(help_text='duration of the quiz in minutes.')
    required_score_to_pass = models.IntegerField(help_text='required score in %.')
    difficulty             = models.CharField(max_length=6, choices=DIFFICULT_CHOICES, default=DIFFICULT_CHOICES[0])
    start_quiz             = models.DateTimeField(null=True, blank=True)
    is_answered            = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}-{self.topic}'


class IntervalQuiz(models.Model):
    quiz         = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    intervalTime = models.TimeField()


    def __str__(self):
        return f'{str(self.quiz)}'




class Question(models.Model):
    quiz               = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question           = models.CharField(max_length=50)
    is_theory_question = models.BooleanField(default=False)
    question_on        = models.DateTimeField(default=timezone.now)
    
    chose1             = models.CharField(max_length=200, null=True, blank=True)
    chose2             = models.CharField(max_length=200, null=True, blank=True)
    chose3             = models.CharField(max_length=200, null=True, blank=True)
    chose4             = models.CharField(max_length=200, null=True, blank=True)
    correct_chosen     = models.CharField(max_length=200, null=True, blank=True)
    
    theory_answer      = models.TextField(max_length=500, null=True, blank=True)
    answerd_on         = models.DateTimeField(default=datetime.datetime.utcnow() + datetime.timedelta(hours=2))
    
    def __str__(self):
        return f'{self.quiz}-{self.question}'

    @classmethod
    def chose_question(cls, quiz_id):
        question = Question.objects.filter(quiz=quiz_id, is_theory_question=False)
        if question.count() == 0:
            return False

        return list(question)

    @classmethod
    def theory_question(cls, quiz_id):
        question = Question.objects.filter(quiz=quiz_id, is_theory_question=True)
        if question.count() == 0:
            return False
        
        return list(question)



class ReportResult(models.Model):
    user = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    question = models.CharField(max_length=255)
    student_answer = models.CharField(max_length=255)
    correct_answer = models.TextField()

    is_true_answered = models.CharField(max_length=50, default='Correct answer')

    question_score = models.FloatField()
    on_date = models.DateTimeField(default=datetime.datetime.utcnow() + datetime.timedelta(hours=2))

    def __str__(self):
        return f'{self.user.id_college}-{self.quiz}'

class TotalDegree(models.Model):
    user = models.ForeignKey(StudentAccount, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    score_to_pass = models.CharField(max_length=50)
    total = models.FloatField()


    def __str__(self):
        return f'{self.user.id_college}-{self.quiz}'
