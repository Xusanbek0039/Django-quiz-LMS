from django.shortcuts import render, redirect
from django.http import JsonResponse
from schedule.models import Material, MaterialVideo, InstructorSchedule, TaskInstructor, TaskStudent, StudentSchedule, \
    Schedule, Post
from users.models import ExtraPermissions, StudentAccount, InstructorAccount, AdminAccount
from django.urls import reverse


def Schedule_view(request, Schedule_Name):
    if request.user.id is None:
        return redirect("home")
    count_std = {
        "std": StudentSchedule.objects.filter(student_schedule_name=Schedule_Name).count(),
        "Material": MaterialVideo.objects.filter(Schedule_name=Schedule_Name).count(),
        "Material_slide": Material.objects.filter(Schedule_name=Schedule_Name).count(),
        "task": TaskInstructor.objects.filter(Schedule_name=Schedule_Name).count(),

    }
    print(count_std)
    context = {
        "Schedule_Name": Schedule_Name,
        "count_std": count_std,
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
        "instructor_Schedule": InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                                 instructor_name=request.user.username),
    }
    return render(request, 'Instructor/ScheduleinStruector.html', context)


def instructor_home(request):
    if request.user.id is None:
        return redirect("home")
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect("home")

    context = {
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
        "instructor_Schedule": InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                                 instructor_name=request.user.username),

    }
    return render(request, 'Instructor/home.html', context)


def Schedule_home(request):
    if request.user.id is None:
        return redirect("home")
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect("home")

    s_c = []
    ins = InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                            instructor_name=request.user.username)
    for iss in ins:
        cour = Schedule.objects.get(company_name=request.user.company_name, schedule_name=iss.instructor_schedule_name)
        x = {"Schedule": iss.instructor_schedule_name, "course": cour.course_name}
        s_c.append(x)

    context = {
        "s_c": s_c,
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
        "instructor_Schedule": InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                                 instructor_name=request.user.username),

    }
    return render(request, 'Instructor/schedule_t.html', context)


def instructor_Material(request, Schedule_Name):
    if request.user.id is None:
        return redirect("home")
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    if request.method == "POST":
        material_name = request.POST['name']
        upload = request.FILES['upload']
        if "choice" in request.POST and request.POST["choice"] == "addvideo":
            MaterialVideo.objects.create(
                material_name=material_name,
                lecture_video=upload,
                company_name=request.user.company_name,
                Schedule_name=Schedule_Name,
            ).save()
        elif "choice" in request.POST and request.POST["choice"] == "addSlide":

            Material.objects.create(
                material_name=material_name,
                slide=upload,
                company_name=request.user.company_name,
                Schedule_name=Schedule_Name,
            ).save()
    context = {
        "viwetask": TaskInstructor.objects.all(),
        "material": MaterialVideo.objects.filter(Schedule_name=Schedule_Name),
        "material_slide": Material.objects.filter(Schedule_name=Schedule_Name),
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
        "Schedule_Name": Schedule_Name,
        "instructor_Schedule": InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                                 instructor_name=request.user.username),

    }
    return render(request, "Instructor/material.html", context)


def delete_material(request, Schedule_Name, id, type):
    if type == "Video":

        delete = MaterialVideo.objects.get(
            id=id,
            Schedule_name=Schedule_Name,

        )
        delete.delete()

    elif type == "slide":

        delete = Material.objects.get(
            id=id,
            Schedule_name=Schedule_Name,
        )
        delete.delete()
    return redirect(reverse("instructor_Material", kwargs={"Schedule_Name": Schedule_Name}))


def delete_task(request, Schedule_Name, id, type):
    if type == "task":
        delete = TaskInstructor.objects.get(
            id=id,
            Schedule_name=Schedule_Name,
        )
        delete.delete()

    return redirect(reverse("instructor_Task", kwargs={"Schedule_Name": Schedule_Name}))


def instructor_Task(request, Schedule_Name):
    if request.user.id is None:
        return redirect("home")
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    if request.method == "POST":
        if "addtask" in request.POST:
            taskname = request.POST['name_task']
            upload = request.FILES['filetask']

            TaskInstructor.objects.create(

                task_name=taskname,
                task_file=upload,
                company_name=request.user.company_name,
                Schedule_name=Schedule_Name,
            ).save()

    context = {
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
        "Schedule_Name": Schedule_Name,
        "instructor_Schedule": InstructorSchedule.objects.filter(instructor_name=request.user.username),
        "viwetask": TaskInstructor.objects.filter(Schedule_name=Schedule_Name),
    }
    return render(request, "Instructor/task.html", context)


def instructor_Schedule(request):
    if request.user.id is None:
        return redirect("home")
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    if 'get' in request.GET:
        InstructorSchedule.objects.create(
            instructor_schedule_name=request.GET["instructor_schedule_name"],
            company_name=request.user.company_name,
            instructor_name=request.user.username,
        ).save()
        Schedule.objects.create(
            schedule_name=request.GET["Schedule_Name"],
            instructor_schedule_name=request.GET["instructor_schedule_name"],
            student_schedule_name=request.GET["student_schedule_name"],
            company_name=request.user.company_name,
            quiz_name=request.GET["quiz_name"],
            task_name=request.GET["task_name"],
            material_name=request.GET["material_name"],
            course_name=request.GET["course_name"],
            post_title=request.GET["post_title"],
        ).save()
        return JsonResponse({"state": True})
    context = {

    }
    return render(request, "Instructor/Schedule.html", context)


def std_open_Schedule(request, Schedule_Name):
    if request.user.id is None:
        return redirect("home")
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    StudentSchedulev = StudentSchedule.objects.filter(company_name=request.user.company_name,
                                                      student_schedule_name=Schedule_Name)

    l = []
    for StudentSchedulev in StudentSchedulev:
        if StudentAccount.objects.filter(username=StudentSchedulev.student_name).exists():
            l.append(StudentAccount.objects.get(username=StudentSchedulev.student_name))

    context = {
        'StudentSchedule': StudentSchedule.objects.filter(student_schedule_name=Schedule_Name),
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
        "instructor_Schedule": InstructorSchedule.objects.filter(instructor_name=request.user.username),
        "studentData": l,
        "Schedule_Name": Schedule_Name,
    }
    return render(request, 'Instructor/student_schedule.html', context)


def ViweTasks(request, Schedule_Name, username):
    if request.user.id is None:
        return redirect("home")
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    print(Schedule_Name, username)
    _std_task = TaskStudent.objects.filter(std_username=username,
                                        std_schedule=Schedule_Name, std_task_d="0")
    if request.method == "POST":
        deg = TaskStudent.objects.get(std_username=username,
                                   std_schedule=Schedule_Name, std_task_name=request.POST.get('itn'))

        deg.std_task_d = int(request.POST.get('degree'))
        deg.save()
    context = {
        "instructor_Schedule": InstructorSchedule.objects.filter(company_name=request.user.company_name,
                                                                 instructor_name=request.user.username),
        "std_task": _std_task,
        "Schedule_Name": Schedule_Name,
        "username": username
    }
    return render(request, "Instructor/v_tasks.html", context)


def detet_task_ans(request,Schedule_Name,username,id ):
  delete=TaskStudent.objects.get(
      id=id,
      std_schedule =Schedule_Name,
      std_username=username,
    )
  delete.delete()
  return redirect(reverse("ViweTasks",kwargs={"Schedule_Name":Schedule_Name,"username":username}))


def report (request,Schedule_Name,username):
    if request.user.id is None:
        return redirect("home")
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')
    degreeAll=0
    TaskdegreeAll= TaskStudent.objects.filter(std_schedule=Schedule_Name,std_username=username)
    print (TaskdegreeAll)
    for i in TaskdegreeAll:
        degreeAll+=i.std_task_d
    print(degreeAll)
    context={
        "reportTask" : TaskStudent.objects.filter(std_schedule=Schedule_Name,std_username=username),
        "degreeAll":degreeAll,
        "Schedule_Name":Schedule_Name,
        "username":username,
        "instructor_Schedule" :InstructorSchedule.objects.filter(instructor_name=request.user.username),
      }
    return render (request,"Instructor/report.html",context)


def post_ins(request, Schedule_Name):
    if request.user.id is None:
        return redirect("home")
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    if request.method == "POST":
        Post.objects.create(
            user_have_post=request.user.username,
            post_title=request.POST.get("titel"),

            post_description=request.POST.get("description"),
            company_name=request.user.company_name,

            Schedule_name=Schedule_Name,
        ).save()
    post = []
    po = Post.objects.filter(Schedule_name=Schedule_Name, company_name=request.user.company_name).order_by(
        "-created_on")
    for po in po:
        if InstructorAccount.objects.filter(username=po.user_have_post).exists():
            d = {
                "user_have_post": po.user_have_post,
                "type": InstructorAccount.objects.get(username=po.user_have_post).instructor_type,
                "name": InstructorAccount.objects.get(
                    username=po.user_have_post).first_name + " " + InstructorAccount.objects.get(
                    username=po.user_have_post).last_name,
                "post_title": po.post_title,
                "post_description": po.post_description,
                "created_on": po.created_on,
            }

            post.append(d)
        if AdminAccount.objects.filter(username=po.user_have_post).exists():
            d = {
                "user_have_post": po.user_have_post,
                "type": AdminAccount.objects.get(username=po.user_have_post).admin_type,
                "name": AdminAccount.objects.get(
                    username=po.user_have_post).first_name + " " + AdminAccount.objects.get(
                    username=po.user_have_post).last_name,
                "post_title": po.post_title,
                "post_description": po.post_description,
                "created_on": po.created_on,
            }
            post.append(d)
    context = {
        "Schedule_Name": Schedule_Name,
        "Post": post,
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),
    }
    return render(request, "Instructor/post.html", context)


def Schedule_student(request, Schedule_Name):
    if request.user.id is None:
        return redirect("home")
    elif not InstructorAccount.objects.filter(username=request.user.username).exists():
        return redirect('home')

    if request.method == "POST":
        StudentSchedule.objects.create(student_schedule_name=Schedule_Name,
                                       company_name=request.user.company_name,
                                       student_name=request.POST.get(""),
                                       )

    context = {
        "Schedule_Name": Schedule_Name,
        "ExtraPermissions": ExtraPermissions.objects.get(user_have_perm=request.user.username),

    }
    return render(request, "Instructor/Schedule_student.html", context)

