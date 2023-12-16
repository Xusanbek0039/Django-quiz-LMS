import json, random

from users.models import InstructorAccount, StudentAccount
from .tasks import check_theory

from django.shortcuts import redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Quiz, Question, ReportResult


def quiz_view(request, schedule_name):
    if not request.user.is_authenticated:
        return redirect('home')

    if (
        not StudentAccount.objects.filter(username=request.user.username).exists() and
        not InstructorAccount.objects.filter(username=request.user.username).exists()
    ):
        return redirect('logout-view')

    context = {}
    context['Schedule_name'] = schedule_name
    expired_num_questions = []

    for quiz in Quiz.objects.filter(is_answered=False, schedule_name=schedule_name, company_name=request.user.company_name):
        theory_q = Question.objects.filter(quiz=quiz, is_theory_question=True)
        chosen_q = Question.objects.filter(quiz=quiz, is_theory_question=False)

        if not quiz.number_of_theory_questions <= theory_q.count() or not quiz.number_of_chosen_questions <= chosen_q.count():
            expired_num_questions.append(quiz.id)

        if quiz.number_of_chosen_questions + quiz.number_of_theory_questions == 0:
            expired_num_questions.append(quiz.id)

    all_quizes = Quiz.objects.exclude(id__in=expired_num_questions).filter(is_answered=False, schedule_name=schedule_name, company_name=request.user.company_name)
    context['all_quizes'] = all_quizes
    context['quiz_list'] = [int(q.id) for q in all_quizes]

    if StudentAccount.objects.filter(username=request.user.username).exists():
        return render(request, 'quiz/quiz_view_st.html', context=context)

    
    

def check_quiz_code_response(request):
    quiz_code = request.GET.get('quiz_code')
    quiz_id   = request.GET.get('quiz_id')

    quiz = Quiz.objects.get(id=quiz_id)
    if quiz.quiz_code == quiz_code:
        return JsonResponse({'true': True})
    else:
        return JsonResponse({'flier': 'Failure quiz code!'})

def question_view(request, *args, **kwargs):
    quiz_id = kwargs['quiz_id']


    context = {}
    quiz_name = Quiz.objects.get(id=quiz_id)

    if ReportResult.objects.filter(user=request.user, quiz=quiz_name).exists():
        return redirect(reverse('quiz-view', kwargs={'schedule_name': kwargs['schedule_name']}))

    context['quiz_name'] = quiz_name.name
    context['quiz_id'] = quiz_id

    theory_question = Question.theory_question(int(quiz_id))
    chose_question  = Question.chose_question(int(quiz_id))

    if theory_question and chose_question:

        random_theory = random.sample(theory_question, k=int(quiz_name.number_of_theory_questions))
        random_chose  = random.sample(chose_question, k=int(quiz_name.number_of_chosen_questions))

        for q in random_chose: random_theory.append(q)
        context['question'] = random_theory
        

    elif theory_question and not chose_question:

        random_theory = random.sample(theory_question, k=int(quiz_name.number_of_theory_questions))
        context['question'] = random_theory

    elif chose_question and not theory_question:

        random_chose = random.sample(chose_question, k=int(quiz_name.number_of_chosen_questions))
        context['question'] = random_chose
    
    return render(request, 'quiz/question_view.html', context=context)

@csrf_exempt
def get_quiz_degree(request):
    data = json.loads(request.POST.get('data_json'))
    quiz_id = request.POST.get('quiz_id')

    dd = {'1': {'answer': 'not_answered', 'is_theory': 'True'},
          '2': {'answer': 'not_answered', 'is_theory': 'True'},
          '5': {'answer': 'not_answered', 'is_theory': 'False'},
          '6': {'answer': 'not_answered', 'is_theory': 'False'},
          '7': {'answer': 'not_answered', 'is_theory': 'False'}
          }

    check_theory.delay(data, request.user, quiz_id)





    return JsonResponse(request.POST.get('data_json'), safe=False)



# student reports #
def reports_views(request, schedule_name):


    report_quiz = ReportResult.objects.filter(user=request.user)
    list_quiz = []
    for x in report_quiz:
        list_quiz.append(x.quiz.id)

    my_quizes = Quiz.objects.filter(id__in=list_quiz, schedule_name=schedule_name)

    return render(request, 'quiz/student_quiz_reports.html', context={'my_quizes': my_quizes, 'Schedule_name': schedule_name})


from .models import TotalDegree
def student_report(request, id, schedule_name):

    my_quiz = Quiz.objects.get(id=id)

    reports = ReportResult.objects.filter(quiz=my_quiz, user=request.user)
    total = TotalDegree.objects.filter(quiz=my_quiz, user=request.user)

    return render(request, 'quiz/student_report.html', context={'reports': reports, 'total': total, 'Schedule_name': schedule_name, 'q_name': my_quiz.name})
