from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .forms import ContactUsForm
from .models import ContactUs, Answer
from users.models import SuperUserAccount


def contact_us_view(request):
    context = {}
    super_users = SuperUserAccount.objects.all()

    form = ContactUsForm()
    context['form'] = form

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            send_mail(
                f'New question from {form.instance.user_email}',
                f'''
                    Question about: {form.instance.about},
                    Description: {form.instance.description}
                
                ''',
                'examle@lms.com',
                [x.email for x in super_users]
            )
            context['done'] = 'We received your question check our blog later or your email'
    return render(request, 'blog/contact_us.html', context=context)


def get_message_unread(request):
    messages = ContactUs.objects.all()
    if request.method == 'POST':
        id = request.POST.get('q_id')
        q_description = request.POST.get('q_description')
        answer = request.POST.get('answer')

        data = ContactUs.objects.get(id=id)
        user_email = data.user_email
        
        send_mail(
            f'We happy for your contact us message, we answered on it!',

            f'''
                Your question about:  {data.about},
                Your explain: {q_description},
                Our answer is: {answer}
            ''',
            request.user.email,
            [user_email]
        )

        Answer.objects.create(
            user_email=user_email,
            question=q_description,
            answer=answer
        )

        data.delete()
    return render(request, 'superuser/messages.html', context={'messages': messages})


@csrf_exempt
def response_message_description(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        data = ContactUs.objects.get(id=id)
        return JsonResponse({'id': data.id, 'description': data.description, 'q_type': data.about})



def blog_view(request):
    answer = Answer.objects.all().order_by('-on_date')
    return render(request, 'blog/blog.html', context={'answer': answer})


@csrf_exempt
def response_blog_id(request):
    id = request.POST.get('id')
    answer = Answer.objects.get(id=id)
    return JsonResponse({'q': answer.question, 'ans': answer.answer})
