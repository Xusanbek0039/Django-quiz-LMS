from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    # ---- std---

    path('Home', views.student_home, name='student_home'),
    path('Schedule/<Schedule_Name>', views.Schedule, name='Schedule'),
    path('Schedule/<Schedule_Name>/Material/video', views.Schedule_Material_video,
         name='Schedule_Material_video'),
    path('Schedule/<Schedule_Name>/Material/Slide', views.Schedule_Material_slide,
         name='Schedule_Material_slide'),
    path('Schedule/<Schedule_Name>/Task', views.Schedule_task, name='Schedule_task'),
    path('Schedule/<Schedule_Name>/Task/ReportTask', views.ReportTask, name='ReportTask'),
    path('Schedule/<Schedule_Name>/AllTask', views.AllTask, name='AllTask'),
    path('Schedule/<Schedule_Name>/Post', views.StudentPost, name='StudentPost'),
    path('schedule_home', views.schedule_home, name='schedule_home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
