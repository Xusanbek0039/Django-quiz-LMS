from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm

from quiz.models import Quiz, Question


class QuizForm(forms.ModelForm):
    time = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Duration in minutes'}))
    required_score_to_pass = forms.IntegerField(label='Score to pass', widget=forms.NumberInput(attrs={'placeholder': 'Score in %'}))    
    start_quiz = forms.DateTimeField(
        help_text=mark_safe('The end of quiz will be (Start quiz + Time), that mean the quiz will remove from the student and the result will be in your Quiz report page.<br><br>In form: <b>YYYY-MM-DD hh:mm:ss</b>'),
        widget=forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD hh:mm:ss'})
        )
    
    class Meta:
        model = Quiz
        fields = [
            'name', 'topic', 'number_of_chosen_questions', 'number_of_theory_questions',
            'time', 'required_score_to_pass', 'difficulty', 'start_quiz', 'quiz_code'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name of quiz'}),
            'quiz_code': forms.TextInput(attrs={'placeholder': 'Code of quiz'}),
            'topic': forms.TextInput(attrs={'placeholder': 'Some of description'}),
            'number_of_chosen_questions': forms.NumberInput(attrs={'placeholder': 'Chosen questions number'}),
            'number_of_theory_questions': forms.NumberInput(attrs={'placeholder': 'Theory questions number'}),
        }
        help_texts = {
            'quiz_code': 'That code\'s student to start the quiz, expired when end of quiz time.',
            'difficulty': 'In default (easy) level, make sure for choice.',
            'number_of_chosen_questions': 'If not assign chosen questions you can assign (0) value.',
            'number_of_theory_questions': 'If not assign theory questions you can assign (0) value.',
        }
        
        labels ={
            'name': 'Quiz name'
        }
    
    def clean_name(self):
        cleaned_data = super().clean()
        name         = cleaned_data.get('name')
        valid        = name.upper()
        return valid




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question', 'chose1',
            'chose2', 'chose3', 'chose4', 'correct_chosen',
            'theory_answer'
        ]
        
        help_texts = {
            'correct_chosen': 'Must be value of: (chose1 or chose2 or chose3 or chose4).',
            'theory_answer': 'The correct answer from you to compare with answer of students.'
        }
        
        widgets = {
            'question': forms.TextInput(attrs={'placeholder': 'Descripe of question...'}),
            'chose1': forms.TextInput(attrs={'placeholder': 'Chose 1..... '}),
            'chose2': forms.TextInput(attrs={'placeholder': 'Chose 2..... '}),
            'chose3': forms.TextInput(attrs={'placeholder': 'Chose 3..... '}),
            'chose4': forms.TextInput(attrs={'placeholder': 'Chose 4..... '}),
            'correct_chosen': forms.TextInput(attrs={'placeholder': 'Correct chosen answer....'}),
            'theory_answer': forms.Textarea(attrs={'placeholder': 'Correct theory answer....'}),
        }