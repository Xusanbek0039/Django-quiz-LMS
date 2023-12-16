from django.urls import path
from . import views

from .schedule_api import (
    InstructorScheduleView, MaterialSlideView,
    CourseView, MaterialVideoView, TaskInstructorView,
    StudentScheduleView

)

urlpatterns = [
    #### users api
    path('companies/',views.GetAllCompanies.as_view()),
    path('companies/signup/',views.GetSignedUpCompanies.as_view()),
    
    path('user/<company_name>/login/<user_type>/',views.LoginApi.as_view()),
    
    path('user/<company_name>/signup/<user_type>/',views.SignUpApi.as_view()),
    
    path('auth-user/',views.AuthUser.as_view()),
    ##################

    #### schedule spi
    path('schedule/instructor/', InstructorScheduleView.as_view()),
    path('schedule/students/<schedule_name>/', StudentScheduleView.as_view()),
    path('schedule/course/<company_name>/<schedule_name>/', CourseView.as_view()),

    path('schedule/material/slide/<schedule_name>/', MaterialSlideView.as_view()),
    path('schedule/material/video/<schedule_name>/', MaterialVideoView.as_view()),

    path('schedule/task/<company_name>/<schedule_name>/', TaskInstructorView.as_view()),
]
