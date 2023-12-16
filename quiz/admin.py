from django.contrib import admin

from .models import Quiz, Question, IntervalQuiz, ReportResult, TotalDegree

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(IntervalQuiz)
admin.site.register(ReportResult)
admin.site.register(TotalDegree)