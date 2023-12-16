import datetime
import json
import random
import string
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse

from quiz.models import Quiz, Question, ReportResult, TotalDegree
from schedule.models import InstructorSchedule
from users.models import InstructorAccount
from .forms import QuizForm, QuestionForm
from .check_num_of_q import check_theory_q, check_chose_q


def create_quiz(request, schedule_name):
    if not request.user.is_authenticated:
        return redirect('home')
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')
    
    context = {}
    ins_schedule = InstructorSchedule.objects.filter(instructor_name=request.user.username)
    context['instructor_Schedule'] = ins_schedule

    quiz_form = QuizForm()
    
    context['quiz_form'] = quiz_form
    context['Schedule_name'] = schedule_name
    
    if request.method == 'POST':
        quiz_name = request.POST.get('name')
        quiz_form = QuizForm(request.POST)
        
        context['quiz_form'] = quiz_form
        
        if quiz_form.is_valid():
            data               = quiz_form.save(commit=False)
            data.user          = request.user
            data.schedule_name = schedule_name
            data.company_name  = request.user.company_name
            data.save()
            
            context['success'] = f'Successfully added quiz:   [  {quiz_name}  ]'
    

    return render(request, 'quiz/create_quiz.html', context=context)

def generate_code(request):
    letters = string.ascii_letters
    for i in range(11):
        letters += str(i)
    code = random.choices(letters, k=10)
    return JsonResponse({'code': ''.join(code)})

def edit_quiz(request, id):
    if not request.user.is_authenticated:
        return redirect('home')
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    
    context = {}
    ins_schedule = InstructorSchedule.objects.filter(instructor_name=request.user.username)
    context['instructor_Schedule'] = ins_schedule

    quiz = Quiz.objects.get(id=id)
    quiz_form = QuizForm(instance=quiz)
    
    context['quiz_form'] = quiz_form
    context['Schedule_name'] = quiz.schedule_name
    
    if request.method == 'POST':
        quiz_name = request.POST.get('name')
        quiz_form = QuizForm(request.POST, instance=quiz)
        
        context['quiz_form'] = quiz_form
        
        if quiz_form.is_valid():
            commit = quiz_form.save(commit=False)
            commit.is_answered = False
            commit.save()
            
            context['success'] = f'Successfully apply quiz:   [  {quiz_name}  ]'
            
            # return redirect('my-quizes-view')
            
    return render(request, 'quiz/edit_quiz.html', context=context)
    


def delete_unanswered_quiz(request, id, schedule_name):
    quiz = Quiz.objects.get(id=id)
    quiz.delete()
    return redirect(reverse('my-quizes-view', kwargs={'schedule_name': schedule_name}))

def my_quizes(request, schedule_name):
    if not request.user.is_authenticated:
        return redirect('home')
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')
    
    context = {}
    ins_schedule = InstructorSchedule.objects.filter(instructor_name=request.user.username)

    context['Schedule_name'] = schedule_name
    context['instructor_Schedule'] = ins_schedule

    form = QuestionForm()
    context['form'] = form
    
    my_quizes = Quiz.objects.filter(user=request.user, schedule_name=schedule_name, company_name=request.user.company_name, is_answered=False)
    context['my_quizes'] = my_quizes
    
    dic_theory  = {}
    for quiz in my_quizes:
        if not check_theory_q(quiz, dic_theory):
            pass
    if len(dic_theory.keys()) != 0:
        context['warning'] = dic_theory.items()

    dic_chose = {}
    for quiz in my_quizes:
        if not check_chose_q(quiz, dic_chose):
            pass
    if len(dic_chose.keys()) != 0:
        context['warning2'] = dic_chose.items()
    
    if request.method == 'POST':

        question_type = request.POST.get('question_type')
        question      = request.POST.get('question')
        quiz_id       = request.POST.get('quiz_id')
        
        form = QuestionForm(request.POST)
        
        if form.is_valid():
            data = form.save(commit=False)
            
            if question_type == 'chosen_q':
                data.is_theory_question = False
            else:
                data.is_theory_question = True
            
            quiz = Quiz.objects.get(id=quiz_id)
            data.quiz = quiz
            data.save()
            
            dic_theory2  = {}
            for quiz in my_quizes:
                if not check_theory_q(quiz, dic_theory2):
                    pass
            if len(dic_theory2.keys()) != 0:
                context['warning'] = dic_theory2.items()
            else:
                try:
                    del context['warning']
                except:
                    pass

            dic_chose2 = {}
            for quiz in my_quizes:
                if not check_chose_q(quiz, dic_chose2):
                    pass
            if len(dic_chose2.keys()) != 0:
                context['warning2'] = dic_chose2.items()
            else:
                try:
                    del context['warning2']
                except:
                    pass
            context['success'] = f'Successfully added {question_type}:   [  {question}  ]'
            
    return render(request, 'quiz/my_quizes.html', context=context)
                

def response_id(request):
    quiz_name = Quiz.objects.get(id=request.GET.get('id'))
    return JsonResponse({'name': quiz_name.name})


def quiz_questions(request, id, schedule_name):
    if not request.user.is_authenticated:
        return redirect('home')
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    ins_schedule = InstructorSchedule.objects.filter(instructor_name=request.user.username)
    
    questions = Question.objects.filter(quiz=id)
    return render(request, 'quiz/quiz_questions.html', context={'questions': questions,'Schedule_name': schedule_name, 'quiz_id': id, 'instructor_Schedule': ins_schedule})


def edit_question(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('home')
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    schedule_name = kwargs['schedule_name']
    quiz_id     = kwargs['quiz_id']
    question_id = kwargs['question_id']
    
    questions = Question.objects.filter(quiz=quiz_id)
    question  = Question.objects.get(id=question_id)
    
    if_theory_q = question.is_theory_question
    
    question_from = QuestionForm(instance=question)

    ins_schedule = InstructorSchedule.objects.filter(instructor_name=request.user.username)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect(reverse('quiz-question', kwargs={'id': quiz_id, 'schedule_name': schedule_name}) )
    
    
    return render(
        request, 'quiz/quiz_questions.html', context=
                  {
                      'questions': questions,
                      'quiz_id': quiz_id,
                      'open_form': True,
                      'if_theory_q': if_theory_q,
                      'question_from': question_from,
                      'Schedule_name': schedule_name,
                      'instructor_Schedule': ins_schedule
                      }
                  )

    
def delete_question(request, *args, **kwargs):
    schedule_name = kwargs['schedule_name']
    quiz_id     = kwargs['quiz_id']
    question_id = kwargs['question_id']
    
    question = Question.objects.get(id=question_id)
    question.delete()
    
    return redirect(reverse('quiz-question', kwargs={'id': quiz_id, 'schedule_name': schedule_name}))    

# Instructor reports

def quizes_report_view(request, schedule_name):
    if not request.user.is_authenticated:
        return redirect('home')
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    ins_schedule = InstructorSchedule.objects.filter(instructor_name=request.user.username)
    
    user = request.user
    my_quizes = Quiz.objects.filter(company_name=user.company_name, schedule_name=schedule_name, is_answered=True)

    if request.method == 'POST':
        quiz = request.POST.get('quiz_id')
        Quiz.objects.get(id=quiz).delete()

    return render(request, 'quiz/my_quizes_report.html', context={'my_quizes': my_quizes, 'Schedule_name': schedule_name, 'instructor_Schedule': ins_schedule})


from django.template.response import TemplateResponse
def report_view(request, id, schedule_name):
    context = {}
    context2 = {}

    my_quiz = Quiz.objects.get(id=id)

    ins_schedule = InstructorSchedule.objects.filter(instructor_name=request.user.username)

    context['q_name'] = my_quiz.name
    context['Schedule_name'] = schedule_name
    context['instructor_Schedule'] = ins_schedule

    context2['q_name'] = my_quiz.name
    context2['Schedule_name'] = schedule_name
    context2['instructor_Schedule'] = ins_schedule

    reports = ReportResult.objects.filter(quiz=my_quiz)
    total   = TotalDegree.objects.filter(quiz=my_quiz)


    dt = {}

    for t in total:
        data = reports.filter(user=t.user)
        dt[data] = t

    context['data'] = dt.items()

    if request.method == 'POST':

        value = request.POST.get('value')

        reports_username = ReportResult.objects.filter(user__username__contains=value, quiz=my_quiz)
        total_username = TotalDegree.objects.filter(user__username__contains=value, quiz=my_quiz)

        reports_id_college = ReportResult.objects.filter(user__id_college__contains=value, quiz=my_quiz)
        total_id_college = TotalDegree.objects.filter(user__id_college__contains=value, quiz=my_quiz)

        dt = dict()

        for t in total_username:
            user_username = reports_username.filter(user=t.user)
            dt[user_username] = t

        for t in total_id_college:
            user_id_college = reports_id_college.filter(user=t.user)
            dt[user_id_college] = t

        context2['data'] = dt.items()

        if total_username:
            return TemplateResponse(request, 'quiz/one_quiz_report.html', context=context2)
        elif total_id_college:
            return TemplateResponse(request, 'quiz/one_quiz_report.html', context=context2)
        else:
            return TemplateResponse(request, 'quiz/one_quiz_report.html', context={'Schedule_name': schedule_name, 'instructor_Schedule': ins_schedule})

    else:
        return TemplateResponse(request, 'quiz/one_quiz_report.html', context=context )

