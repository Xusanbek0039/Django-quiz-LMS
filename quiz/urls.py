from django.urls import path
from . import views



urlpatterns = [
    path('quizes/<schedule_name>/', views.quiz_view, name='quiz-view'),
    path('response/code/', views.check_quiz_code_response),

    path('questions/<quiz_id>/<schedule_name>/', views.question_view, name='questions'),


    path('get-quiz-degree/', views.get_quiz_degree),
    path('reports/<schedule_name>/', views.reports_views, name='quiz-reports-view'),

    path('report/<id>/<schedule_name>/', views.student_report, name='report-view'),
]
