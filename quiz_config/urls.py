from django.urls import path

from . import views


urlpatterns = [
    
    path('add/quiz/<schedule_name>/', views.create_quiz, name='add-quiz'),
    path('response_code/', views.generate_code),

    path('delete/unanswerd/quiz/<id>/<schedule_name>/', views.delete_unanswered_quiz, name='delete-unanswerd-quiz'),
    
    path('quiz/my-quizes/<schedule_name>/', views.my_quizes, name='my-quizes-view'),
    path('quiz/my-quizes/edit/<id>/', views.edit_quiz, name='edit-quiz'),
    path('response_id/', views.response_id),
    
    path('quiz/my-quizes/quiz-question/<id>/<schedule_name>/', views.quiz_questions, name='quiz-question'),
    
    path('quiz/my-quizes/quiz-question/<quiz_id>/question/edit/<question_id>/<schedule_name>/', views.edit_question, name='edit-question'),
    path('quiz/my-quizes/quiz-question/<quiz_id>/question/delete/<question_id>/<schedule_name>/', views.delete_question, name='delete-question'),

    
    path('reports/<schedule_name>/', views.quizes_report_view, name='reports-view'),
    path('report/<id>/<schedule_name>/', views.report_view, name='report-one'),
]