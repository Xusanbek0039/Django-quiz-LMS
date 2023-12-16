from schedule.models import (
    Post, Material, MaterialVideo,
    TaskInstructor, TaskStudent,
    InstructorSchedule, StudentSchedule,
    Schedule, Course
)

from rest_framework import serializers

class InstructorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorSchedule
        fields = '__all__'

class StudentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSchedule
        fields = '__all__'

class GetCourse(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class GetMaterialSlide(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class GetMaterialVideo(serializers.ModelSerializer):
    class Meta:
        model = MaterialVideo
        fields = '__all__'

class GetTaskInstructor(serializers.ModelSerializer):
    class Meta:
        model = TaskInstructor
        fields = '__all__'
