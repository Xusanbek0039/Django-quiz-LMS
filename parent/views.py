
from django.shortcuts import render

from quiz.models import ReportResult, Quiz, TotalDegree
from users.models import StudentAccount
from schedule.models import StudentSchedule,Schedule
from schedule.models import TaskStudent

def parent_home (request  ):


  return render(request ,"parent/home.html" )
def parent_student (request  ):
  list=[]
  list2=[]
  student=StudentAccount.objects.filter(parent_national_id=request.user.national_id)

  # studentschedule = StudentSchedule.objects.filter(student_schedule_name=student.username)
  for student in student :
    list=[]
    # print(student)
    studentschedule = StudentSchedule.objects.filter(student_name=student.username)
    
    for  studentschedule in studentschedule:
      # print(studentschedule)
      
      list.append({
        "studentschedule":Schedule.objects.get(schedule_name=studentschedule.student_schedule_name),
      })

    d={
      "student":student,
      "schedule":list,
    }
    list2.append(d)
    print(list2)
  context={
    "l":StudentAccount.objects.filter(parent_national_id=request.user.national_id),
    "data":list2,
    }

  return render(request ,"parent/student.html", context)
def parent_schedule (request,Schedule_name ,username ,company_name ):
  
  std = StudentAccount.objects.get(username=username)
  report_quiz = ReportResult.objects.filter(user=std.id)
  list_quiz = []
  for x in report_quiz:
    list_quiz.append(x.quiz.id)

  my_quizes = Quiz.objects.filter(id__in=list_quiz, schedule_name=Schedule_name)
  print(my_quizes)
  # print(Schedule_name+"\n"+username+"\n"+company_name)
  list=[]
  n=1
  sum=0
  for x in TaskStudent.objects.filter(std_schedule=Schedule_name,std_username=username,std_company=company_name):

    sum=sum+int(x.std_task_d)
    list.append({
      "task_report":x,
      "n":n,
     
    })
    n=n+1
  context={
    "task_report":list,
    "sum":sum,
    "my_quizes": my_quizes,
    "username": username,
    "schedule_name": Schedule_name
  }

  return render(request ,"parent/schedule.html" ,context)











def student_quiz_report(request, username, id):
  my_quiz = Quiz.objects.get(id=id)
  std = StudentAccount.objects.get(username=username)
  reports = ReportResult.objects.filter(quiz=my_quiz, user=std.id)
  total = TotalDegree.objects.filter(quiz=my_quiz, user=std.id)

  return render(request, 'parent/quiz_report.html',
                context={'reports': reports, 'total': total, 'q_name': my_quiz.name})