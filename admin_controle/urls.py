from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # admin
    path('', views.home_admin, name='home_admin'),
    path('adminCompany/Schedule', views.Schedule_admin, name='Schedule_admin'),
    path('adminCompany/course', views.Course_admin, name='course_admin'),
    path('adminCompany/Schedule instructor', views.Schedule_instructor_admin, name='Schedule_instructor_admin'),
    path('adminCompany/Schedule student', views.Schedule_student, name='Schedule_student_admin'),

    path('adminCompany/Manage Schedule/<ScheduleName>', views.manage_Schedule, name='manage_Schedule'),
    path('adminCompany/Manage Schedule/<ScheduleName>/delete/<username>/<type>', views.delete_user_Schedule,
         name='delete_user_Schedule'),
    path('adminCompany/Manage Schedule/<ScheduleName>/Deleted', views.delete_Schedule, name='delete_Schedule'),
    # management
    path('adminCompany/Manage Admin', views.manage_admin, name='manage_admin'),
    path('adminCompany/Manage Admin/delete/<id>/<username>/', views.deleteadmin, name='DeleteAdmin'),

    path('adminCompany/Manage Instructor', views.manage_instructor, name='manage_instructor'),
    path('adminCompany/Manage Instructor/delete/<id>/<username>', views.deleteinstuctor, name='deleteinstuctor'),

    path('adminCompany/Manage Student', views.manage_Student, name='manage_Student'),
    path('adminCompany/Manage Student/delete/<id>', views.deletestudent, name='deletestudent'),

    path('adminCompany/Manage Parent', views.manage_parent, name='manage_parent'),
    path('adminCompany/Statistics', views.Statistics, name='Statistics'),
    # Request User
    path('adminCompany/Request Instructor', views.Request_instructor, name='Request_instructor'),
    path('adminCompany/Request Student', views.Request_Student, name='Request_Student'),

    # profile Admin
    path('adminCompany/Manage Schedule/<ScheduleName>/Post', views.admin_post,name='admin_post'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )

