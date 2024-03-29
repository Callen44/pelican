import datetime
import os

from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .views import update
from .models import Post, Like, Comment


class PostTests(TestCase):
    def setUp(self):
        # creates a user and logs into the client
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.force_login(self.user)

    def test_update_view(self):
        # tests the view that updates posts
        posts = [Post.objects.create(title='title', body='blank', published_date=timezone.now(), created_by=self.user) for _ in range(2)]
        p1 = posts[0]

        data = {
            'title': 'I am a mongoose',
            'body': 'it is true',
        }
        response = self.client.post(f'/{p1.id}/update/', data=data)

        self.assertEqual(response.status_code, 302)

        p1.refresh_from_db()
        self.assertEqual(p1.title, 'I am a mongoose')

    def test_index_view(self):
        # checks that the index view responds with 200

        # yes I know this test could be better, like
        # testing things like the info provided that is
        # shown. but these are my first posts, and I am
        # not shure how this should be best adapted in
        # the future
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_delete_view(self):
        # deletes a post to make sure the view works
        posts = [Post.objects.create(title='title', body='blank', published_date=timezone.now(), created_by=self.user) for _ in range(2)]
        p1 = posts[0]

        response = self.client.get(f'/{p1.id}/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=p1.id).exists())
    def test_create_view(self):
        # this tests the create view

        data = {
            'title': 'I exist',
            'body': "If I don't then something is wrong",
        }
        response = self.client.post('/create/', data=data)
        
        # check for the post
        assert Post.objects.filter(title='I exist').exists()
    def test_like_view(self):
        # make a post
        p1 = Post.objects.create(title='title', body='body', published_date=timezone.now(), created_by=self.user)

        # send POST request 
        response = self.client.get(f'/{str(p1.id)}/like')

        # check that the response status code is 302, indicating a redirect
        self.assertEqual(response.status_code, 302)

        # check that a Like object was created
        self.assertTrue(Like.objects.filter(posts=p1).exists())
    def test_comment_view(self):
        # make a post
        p1 = Post.objects.create(title='title', body='body', published_date=timezone.now(), created_by=self.user)

        # prepare data to be sent
        data = {
            'post_id': str(p1.id),
            'comment': 'this is a test comment',
        }

        # make the request
        response = self.client.post('/', data=data)

        # check the response worked
        self.assertEqual(response.status_code, 200)
        
        # check for the comment
        self.assertTrue(Comment.objects.filter(post=p1).exists())
    def test_comment_delete(self):
        # make a post
        p1 = Post.objects.create(title='title', body='body', published_date=timezone.now(), created_by=self.user)

        # make a comment
        c1 = Comment.objects.create(comment="hello", post=p1, user=self.user, published_date = timezone.now())

        # delete comment
        response = self.client.get(f'/{c1.id}/{p1.id}/delete_comment')

        # check the response worked
        self.assertEqual(response.status_code, 302)

        # check for the comment
        self.assertFalse(Comment.objects.filter(post=p1).exists())