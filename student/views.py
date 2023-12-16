from django.shortcuts import render
from schedule.models import StudentSchedule, MaterialVideo, InstructorSchedule, TaskInstructor, TaskStudent, \
    Schedule as _Schedule, Material, Post
from users.models import InstructorAccount, ExtraPermissions


def schedule_home(request):
    ins = []
    std_schedule = StudentSchedule.objects.filter(company_name=request.user.company_name,
                                                  student_name=request.user.username)

    for std_schedule in std_schedule:
        ins_schedule1 = InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                          instructor_schedule_name=std_schedule.student_schedule_name)
        schedule = _Schedule.objects.get(company_name=request.user.company_name,
                                         schedule_name=std_schedule.student_schedule_name)
        inn = []
        for ins_schedule1 in ins_schedule1:
            if InstructorAccount.objects.filter(company_name=request.user.company_name,
                                                username=ins_schedule1.instructor_name).exists():
                ins_account1 = InstructorAccount.objects.get(company_name=request.user.company_name,
                                                             username=ins_schedule1.instructor_name)

                D = {
                    "Instructor_type": ins_account1.instructor_type,
                    "Instructor_name": ins_account1.first_name + " " + ins_account1.last_name,
                    "Instructor_username": ins_account1.username,
                }

                inn.append(D)
        if inn:
            s_bt = True
        else:
            s_bt = False
        x = {
            "std_schedule": std_schedule.student_schedule_name,
            "course_name": schedule.course_name,
            "inst": inn,
            "s_bt": s_bt
        }
        ins.append(x)
        print(ins)

    context = {
        "d": ins,
        "StudentSchedule": StudentSchedule.objects.filter(student_name=request.user.username),
    }

    return render(request, "student/schedule_home.html", context)


def AllTask(request, Schedule_Name):
    if request.method == "POST":
        taskname = request.POST.get('itn')
        upload = request.FILES['uf']

        TaskStudent.objects.create(
            std_username=request.user.username,
            std_company=request.user.company_name,
            std_task_name=taskname,
            std_schedule=Schedule_Name,
            std_task_file=upload,
            std_task_d=0,
            is_download=True,
        ).save()
    ans_std_task = TaskStudent.objects.filter(std_schedule=Schedule_Name, std_company=request.user.company_name,
                                           std_username=request.user.username)
    xx = []
    a_ans_std_task = []
    for ans_std_task in ans_std_task:
        a_ans_std_task.append(ans_std_task.std_task_name)

    std_task = TaskInstructor.objects.filter(Schedule_name=Schedule_Name, company_name=request.user.company_name)
    for std_task in std_task:
        if a_ans_std_task.count(str(std_task.task_name)) == 0:
            print(std_task)
            d = {
                "ans_task": std_task,
            }
            xx.append(d)

    context = {
        "StudentSchedule": StudentSchedule.objects.filter(student_name=request.user.username),
        "ScheduleStudent": Schedule_Name,
        "task": xx,
        "ans_task": TaskStudent.objects.filter(std_schedule=Schedule_Name, std_company=request.user.company_name,
                                            std_username=request.user.username, )
    }
    return render(request, "student/da_task.html", context)

def student_home (request):

  context={
  "StudentSchedule":StudentSchedule.objects.filter(student_name=request.user.username),
  }
  return render(request,"student/home.html",context)


def Schedule(request, Schedule_Name):
    ins_s = InstructorSchedule.objects.filter(instructor_schedule_name=Schedule_Name)

    context = {
        "StudentSchedule": StudentSchedule.objects.filter(student_name=request.user.username),
        "ScheduleStudent": Schedule_Name
    }

    for ins_s in ins_s:
        if ExtraPermissions.objects.filter(user_have_perm=ins_s.instructor_name, company_name=request.user.company_name).exists():
            inst_ext = ExtraPermissions.objects.get(user_have_perm=ins_s.instructor_name, company_name=request.user.company_name)
            context['ExtraPermissions'] = inst_ext
    li = (TaskStudent.objects.filter(std_schedule=Schedule_Name, std_company=request.user.company_name,
                                  std_username=request.user.username, ))
    lis = []

    for li in li:
        l = {"taskname": li.std_task_name, "degree_p": li.std_task_d * 10, "degree": li.std_task_d}
        lis.append(l)

    context['ans_task'] = lis


    return render(request, "student/schedule.html", context)


def Schedule_Material_video (request,Schedule_Name):
  context={
    "StudentSchedule":StudentSchedule.objects.filter(student_name=request.user.username),
    "Material_video":MaterialVideo.objects.filter(Schedule_name=Schedule_Name),
    'ScheduleStudent':Schedule_Name,
  }
  return render ( request,"student/videomat.html",context)


def Schedule_Material_slide (request,Schedule_Name):
  Material_slide=Material.objects.filter(company_name=request.user.company_name,Schedule_name=Schedule_Name)
  x=0
  m=[]
  for i  in Material_slide:
    x+=1
    d={
      "x":x,
      "material_name":i.material_name,
      "slide":i.slide,

    }
    m.append(d)
  context={
  "StudentSchedule":StudentSchedule.objects.filter(student_name=request.user.username),
 "Material_slide":m,
 "Schedule_Name":Schedule_Name,
}
  return render ( request,"student/slide.html",context)


def Schedule_task (request,Schedule_Name ):
  if request.method=="POST":
    taskname=request.POST.get('itn')
    upload=request.FILES['uf']

    TaskStudent.objects.create(
      std_username  =  request.user.username,
      std_company   =  request.user.company_name,
      std_task_name =  taskname ,
      std_schedule  =  Schedule_Name,
      std_task_file =  upload,
      std_task_d   =  0,
      is_download   =  True,
    ).save()
  context={
    "StudentSchedule":StudentSchedule.objects.filter(student_name=request.user.username),
    "ScheduleStudent":Schedule_Name,
    "task":TaskInstructor.objects.filter(Schedule_name=Schedule_Name,company_name=request.user.company_name),
    "ans_task":TaskStudent.objects.filter(std_schedule=Schedule_Name,std_company=request.user.company_name,std_username=request.user.username,)
  }
  return render ( request,"student/task.html",context)


def ReportTask(request, Schedule_Name):
    context = {
        "ans_task": TaskStudent.objects.filter(std_schedule=Schedule_Name, std_company=request.user.company_name,
                                            std_username=request.user.username, std_task_d__gt=0),
        "ScheduleStudent": Schedule_Name,
    }
    return render(request, "student/reporttask.html", context)


def StudentPost(request, Schedule_Name):
    post = []
    po = Post.objects.filter(Schedule_name=Schedule_Name, company_name=request.user.company_name).order_by(
        "-created_on")
    for po in po:
        if InstructorAccount.objects.filter(username=po.user_have_post).exists():
            d = {
                "type": InstructorAccount.objects.get(username=po.user_have_post).instructor_type,
                "name": InstructorAccount.objects.get(
                    username=po.user_have_post).first_name + " " + InstructorAccount.objects.get(
                    username=po.user_have_post).last_name,
                "post_title": po.post_title,
                "post_description": po.post_description,
                "created_on": po.created_on,
            }
            post.append(d)
    context = {
        "ScheduleStudent": Schedule_Name,
        "Post": post,
    }
    return render(request, "student/post.html", context)