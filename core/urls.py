from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('super/', include('superuser.urls')),
    path('users/', include('users.urls')),
    path('', include('admin_controle.urls')),
    path('instructor/', include('instructor.urls')),
    path('student/', include('student.urls')),
    path('Parent/', include('parent.url')),


    path('quiz-conf/', include('quiz_config.urls')),
    path('quiz/', include('quiz.urls')),



    path('api-user/', include('userapi.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
