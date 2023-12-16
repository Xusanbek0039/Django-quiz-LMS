from pyexpat import model
from django.conf import Settings, settings
from django.urls import path
from django.conf.urls.static  import static
from django.conf  import settings
from . import views 

from django.contrib.auth import views as auth_views
urlpatterns = [

  path('Home',views.parent_home,name='parent_home'),
  path('',views.parent_home,name='parent_home'),

  path('My Sons',views.parent_student,name='parent_student'),
  path('My Children',views.parent_student,name='parent_student'),


  path('My Sons/Schedule',views.parent_schedule,name='parent_schedule'),
  path('My Children/Schedule/<Schedule_name> #\ <username> \# <company_name>',views.parent_schedule,name='parent_schedule'),
  path('My children/<username>/quiz/report/<id>/', views.student_quiz_report, name='my-chil-quiz-report')
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)