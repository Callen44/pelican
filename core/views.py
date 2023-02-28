from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Count

from .models import Post, Like

# Create your views here.
def index(request):
    posts = Post.objects.order_by("-published_date").annotate(num_likes=Count("likes"))
    return render(request, 'home.html', {'posts': posts})
def like(request, pk):
    #users cannot like posts that they have allready liked in the past
    post = Post.objects.get(id=pk)
    
    l = Like(users = request.user, posts = post)
    all_likes = Like.objects.all()
    for like in all_likes:
        if l.users == like.users and l.posts == like.posts:
            return HttpResponseRedirect('..')
    l.save()
    return HttpResponseRedirect('..')
def update(request, pk):
    post = request.POST
    post_got = Post.objects.get(id=pk)
    if post_got.created_by == request.user:
        if post != {}:
            post_got.post_title = post['title']

            post_got.post_body = post['body']
            post_got.save()

            return HttpResponseRedirect('../..')
        else:
            post_dat = {'title': post_got.title, 'author_id': str(post_got.created_by), 'created': post_got.published_date, 'body': post_got.body, 'id': post_got.id}
            return render(request, 'update.html', {'post': post_dat})
    else:
        return HttpResponseRedirect('../..')
def create(request):
    post = request.POST
    if post != {}:
        p = Post(title = post['title'], body = post['body'], published_date = timezone.now(), created_by=request.user)
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