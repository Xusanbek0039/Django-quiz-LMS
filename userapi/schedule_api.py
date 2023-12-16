from schedule.models import (
    Post, Material, MaterialVideo,
    TaskInstructor, TaskStudent,
    InstructorSchedule, StudentSchedule,
    Schedule, Course
)

from .schedule_serializers import (
    InstructorScheduleSerializer, StudentScheduleSerializer,
    GetMaterialSlide, GetCourse,
    GetMaterialVideo, GetTaskInstructor
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class InstructorScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def get(self, request):
        instructor_schedule = InstructorSchedule.objects.filter(instructor_name=request.user.username)
        serial = InstructorScheduleSerializer(instance=instructor_schedule, many=True)
        return Response(serial.data)

class StudentScheduleView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def get(self, request, schedule_name):
        student_schedule = StudentSchedule.objects.filter(company_name=request.user.company_name, student_schedule_name=schedule_name)
        serial = StudentScheduleSerializer(instance=student_schedule, many=True)
        return Response(serial.data)


class CourseView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def get(self, request, company_name, schedule_name):
        schedule = Schedule.objects.filter(company_name=company_name, schedule_name=schedule_name)
        course   = Course.objects.filter(course_name__in=[x.course_name for x in schedule])

        serial = GetCourse(instance=course, many=True)

        return Response(serial.data)

class MaterialSlideView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def get(self, request, schedule_name):
        slides = Material.objects.filter(Schedule_name=schedule_name)
        serial = GetMaterialSlide(instance=slides, many=True)
        return Response(serial.data)

    def post(self, request, schedule_name):
        material_name = request.data.get('material_name')
        slide = request.FILES.get('slide')

        Material.objects.create(
            material_name=material_name,
            Schedule_name=schedule_name,
            slide=slide,
            company_name=request.user.company_name,
        )

        return Response({'success': 'Created!'})

class MaterialVideoView(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    def get(self, request, schedule_name):
        lecture_video = MaterialVideo.objects.filter(Schedule_name=schedule_name)
        serial = GetMaterialVideo(instance=lecture_video, many=True)
        return Response(serial.data)

    def post(self, request, schedule_name):
        material_name = request.data.get('material_name')
        lecture_video = request.FILES.get('lecture_video')

        MaterialVideo.objects.create(
            material_name=material_name,
            Schedule_name=schedule_name,
            lecture_video=lecture_video,
            company_name=request.user.company_name,
        )

        return Response({'success': 'Created!'})

class TaskInstructorView(APIView):

    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request, company_name, schedule_name):
        schedule = InstructorSchedule.objects.filter(instructor_schedule_name=schedule_name, instructor_name=request.user.username)
        task = TaskInstructor.objects.filter(company_name=company_name, Schedule_name__in=[x.instructor_schedule_name for x in schedule])
        serial = GetTaskInstructor(instance=task, many=True)
        return Response(serial.data)

    def post(self, request, company_name, schedule_name):
        task_name = request.data.get('task_name')
        task_file = request.FILES.get('task_file')

        TaskInstructor.objects.create(
            task_name=task_name,
            task_file=task_file,
            company_name=company_name,
            Schedule_name=schedule_name
        )
        return Response({'success': 'Created!'})
