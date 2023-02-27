from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Count

from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.order_by("-published_date").annotate(num_likes=Count("likes"))
    print(posts[0].created_by)
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