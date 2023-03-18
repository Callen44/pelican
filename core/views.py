from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from .models import Post, Like, Comment

# Create your views here.
def index(request):
    # check if there is any incomming data (comments) and make sure the user is authenticated
    POST = request.POST
    if POST != {} and request.user.is_authenticated:
        # a comment has been recived, time to move forward with creating it

        # figure out if the post even exists
        get_object_or_404(Post, id = POST['post_id'])

        # grab the user object
        user_active = User.objects.get(id = POST['user'])

        # grab the post object
        post_active = Post.objects.get(id = POST['post_id'])

        # make and save the comment
        n_comment = Comment(user = user_active, comment = POST['comment'], post = post_active)
        n_comment.save()

    posts = Post.objects.order_by("-published_date").annotate(num_likes=Count("likes"))
    return render(request, 'home.html', {'posts': posts})
@login_required
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
@login_required
def update(request, pk):
    post = request.POST
    post_got = Post.objects.get(id=pk)
    if post_got.created_by == request.user:
        if post != {}:
            post_got.title = post['title']

            post_got.body = post['body']
            post_got.save()

            return HttpResponseRedirect('../..')
        else:
            post_dat = {'title': post_got.title, 'author_id': str(post_got.created_by), 'created': post_got.published_date, 'body': post_got.body, 'id': post_got.id}
            return render(request, 'update.html', {'post': post_dat})
    else:
        return HttpResponseRedirect('../..')
@login_required
def create(request):
    post = request.POST
    if post != {}:
        p = Post(title = post['title'], body = post['body'], published_date = timezone.now(), created_by=request.user)
        p.save()
        p = None

        return HttpResponseRedirect('../')
    else:
        return render(request, 'create.html')
@login_required
def delete(request, pk):
    post = Post.objects.get(id=pk)
    if request.user == post.created_by:
        post.delete()
    return HttpResponseRedirect('../..')