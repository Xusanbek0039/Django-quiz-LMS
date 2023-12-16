from django.urls import path
from . import views
from superuser.blog import contact_us_view, blog_view, response_blog_id






urlpatterns = [
    path("make-request/", views.make_request, name="make-request"),
    path("", views.home_view, name="home"),
    path("become/company/", views.become_partener_home, name="become-company"),
    path("companies/", views.companies_view, name="companies-view"),
    path("type/<company_name>/", views.type_view, name="type-view"),
    
    path("login/<str:company_name>/<str:type_user>/", views.login_view, name="login-view"),
    path("login/<str:company_name>/<str:type_user>/signup/", views.sign_up_instructor_view, name="signup-ins-view"),
    path("login/<str:company_name>/<str:type_user>/signup/st/", views.sign_up_student_view, name="signup-stu-view"),
    path('logout/', views.logout_view, name='logout-view'),

    path('my-info/', views.edit_user_data, name='my-info'),
    path('my-pass/', views.edit_user_pass, name='my-pass'),

    # blog
    path('contact-us/', contact_us_view, name='contact-us'),
    path('blog/', blog_view, name='blog'),
    path('response/blog/', response_blog_id),

    # reset password
    path('request-reset-email/', views.request_password_reset),
    path('reset-pass-complete/<token>/', views.reset_complete, name='password_reset_complete'),
]
