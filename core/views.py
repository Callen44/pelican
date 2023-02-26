from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from .models import Post

# Create your views here.
def index(request):
    posts = []
    
    for post in Post.objects.order_by('-pub_date'):
        posts.append({'title': post.get_name(), 'author_id': str(post.get_author()), 'created': post.get_date(), 'body': post.get_body(), 'id': post.get_id()})
        #print(post.get_likes())
    return render(request, 'home.html', {'posts': posts})
def update(request, pk):
    post = request.POST
    post_got = Post.objects.get(id=pk)
    if post_got.get_author() == request.user:
        if post != {}:
            post_got.post_title = post['title']

            post_got.post_body = post['body']
            post_got.save()

            return HttpResponseRedirect('../..')
        else:
            post_dat = {'title': post_got.get_name(), 'author_id': str(post_got.get_author()), 'created': post_got.get_date(), 'body': post_got.get_body(), 'id': post_got.get_id()}
            return render(request, 'update.html', {'post': post_dat})
    else:
        return HttpResponseRedirect('../..')
def create(request):
    post = request.POST
    if post != {}:
        p = Post(post_title = post['title'], post_body = post['body'], pub_date = timezone.now(), by=request.user)
        p.save()
        p = None

        return HttpResponseRedirect('../')
    else:
        return render(request, 'create.html')
def delete(request, pk):
    post = Post.objects.get(id=pk)
    if request.user == post.get_author():
        post.delete()
    return HttpResponseRedirect('../..')