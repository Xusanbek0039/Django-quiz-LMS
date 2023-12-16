from django.db import models
from django.utils import timezone

class ContactUs(models.Model):
    ABOUT_CHOICES = [
        ('become_company', 'About.. become company'),
        ('admin', 'About.. as admin'),
        ('instructor', 'About.. as Instructor'),
        ('student', 'About.. as student'),
        ('parent', 'About.. as parent'),
        ('course', 'About.. course'),
        ('quiz', 'About.. quiz'),
    ]
    user_email = models.EmailField()
    about = models.CharField(max_length=50, choices=ABOUT_CHOICES)
    description = models.TextField()


    def __str__(self):
        return f'{self.user_email}:{self.about}'

class Answer(models.Model):
    user_email = models.EmailField()
    question = models.TextField()
    answer = models.TextField()
    on_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.user_email
