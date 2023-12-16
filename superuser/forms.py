from django import forms
from .models import ContactUs, Answer


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'

        labels = {
            'user_email': 'Your email'
        }

        widgets = {
            'user_email': forms.TextInput(attrs={'placeholder': 'example@example.com'}),
            'description': forms.Textarea(attrs={'placeholder': 'Your explain'}),
        }
