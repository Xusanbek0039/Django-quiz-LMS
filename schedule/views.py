from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from schedule.models import Post
from .form import PostForm



def admin_page(request):
    posts = Post.objects.all()
    return render(request, 'admin.html', context={'form': PostForm(), 'posts': posts})





def admin_set_post(request):
    if request.method == 'POST':
        if Post.objects.filter(user_have_post=request.POST.get('user_have_post')).exists():
            return JsonResponse({'user': 'created before'})
        
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # print(request.FILES.get('post_file'))
            print(form.instance.user_have_post)
            print(form.instance.post_file.url)
            print(form.instance.id)
            
            return JsonResponse({'posted': 1})

def admin_edit_post(request, id):
    post = Post.objects.get(id=id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
    return render(request, 'edit_post.html', context={'form': form})

