from django.utils import timezone
from django.db import models


class Post(models.Model):
    user_have_post = models.CharField(max_length=50)
    post_title = models.CharField(max_length=30)
    Schedule_name    = models.CharField(max_length=50)
    post_file = models.FileField(upload_to='posts/%Y/%m/%d/')
    post_description = models.TextField()
    company_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_have_post


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course_name


class Material(models.Model):
    material_name = models.CharField(max_length=20)
    Schedule_name = models.CharField(max_length=50)
    slide = models.FileField(upload_to='materials/slide/%Y/%m/%d/')
    company_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.material_name


class MaterialVideo(models.Model):
    material_name = models.CharField(max_length=20)
    Schedule_name = models.CharField(max_length=50)
    lecture_video = models.FileField(upload_to='materials/videos/%Y/%m/%d/')
    company_name  = models.CharField(max_length=50)
    created_on    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.material_name


class TaskInstructor(models.Model):
    task_name     = models.CharField(max_length=50)
    task_file     = models.FileField(upload_to='tasks/%Y/%m/%d/')
    company_name  = models.CharField(max_length=50)
    Schedule_name = models.CharField(max_length=50)
    created_on    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.task_name

class TaskStudent (models.Model):
    std_username  =  models.CharField(max_length=40)
    std_company   =  models.CharField(max_length=40)
    std_task_name =  models.TextField()
    std_schedule  =  models.TextField()
    std_task_file =  models.FileField(upload_to='tasks/ans/%Y/%m/%d/')
    std_task_d    =  models.IntegerField()
    is_download   =  models.BooleanField(default=False)

    def __str__(self):
        return self. std_schedule


class InstructorSchedule(models.Model):
    instructor_schedule_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    instructor_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.instructor_schedule_name} : {self.company_name}'


class StudentSchedule(models.Model):
    student_schedule_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    student_name = models.CharField(max_length=30)
    can_post = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student_schedule_name} : {self.company_name}'


class Schedule(models.Model):
    schedule_name = models.CharField(max_length=30, unique=True)
    company_name = models.CharField(max_length=50)
    course_name  = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.schedule_name} : {self.company_name}'