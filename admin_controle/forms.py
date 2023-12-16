from django import forms
from users.models import (
    AdminAccount, ExtraPermissions,
    StudentAccount, InstructorAccount,
    ParentAccount
)
from schedule.models import(
    Material, Post, Course,
    TaskInstructor, Quiz, Schedule,
)

class post_form (forms.ModelForm):
    class Meta:
        model = Post
        fields =["user_have_post","post_title","post_file","post_description"]

        widgets = {
            'user_have_post': forms.TextInput(attrs={'placeholder': 'post\'s user'}),
            'post_title': forms.TextInput(attrs={'placeholder': 'post\'s title'}),
            'post_description': forms.Textarea(attrs={'placeholder': 'post\'s description'}),
        }


class Admin_form (forms.ModelForm):
    class Meta:
        model = AdminAccount
    
        fields = '__all__'


class Course_form (forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class student_form (forms.ModelForm):
    class Meta:
        model = StudentAccount
        fields = '__all__'

class instractor_form (forms.ModelForm):
    class Meta:
        model = InstructorAccount
        fields = '__all__'


class scedulee_form (forms.ModelForm):
    class Meta:
        model = Schedule
    
        fields = '__all__'
       