from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_page, name='admin-home'),
    path('post/', views.admin_set_post, name='admin-setpost'),
    
    path('edit/post/<id>/', views.admin_edit_post, name='admin-edit-post'),
    
]
