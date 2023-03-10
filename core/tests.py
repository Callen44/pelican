import datetime
import os

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client

from .views import update
from .models import Post, Like


class postTests(TestCase):

    def test_update_view(self):
        # Create a test user and log them in
        user = User.objects.create_user(username='testuser', password='testpass')
        client = Client()
        client.force_login(user)

        # Create two posts
        p1 = Post.objects.create(title='title', body='blank', published_date=timezone.now(), created_by=user)
        p2 = Post.objects.create(title='title', body='blank', published_date=timezone.now(), created_by=user)

        # Get a CSRF token
        response = client.get(f'/{p1.id}/update/')
        csrf_token = response.cookies['csrftoken'].value

        # Update p1 with new data
        data = {
            'title': 'I am a mongoose',
            'body': 'it is true',
            'csrfmiddlewaretoken': csrf_token,
        }
        response = client.post(f'/{p1.id}/update/', data=data)

        # Check that the response status code is 302, indicating a redirect
        assert response.status_code == 302

        #Check that the updated post has the correct title
        p1.refresh_from_db()
        assert p1.title == 'I am a mongoose'


    def test_index_view(self):
        # activate the client
        client = Client()

        # make a test user
        user = User.objects.create_user(username='testuser', password='testpass')
        client.force_login(user)

        # create the 2 posts
        p1 = Post(title = "title", body = "blank", published_date = timezone.now(), created_by = user)
        p1.save()
        
        # the seccond post uses the same title
        p2 = Post(title = "title", body = "blank", published_date = timezone.now(), created_by = user)
        p2.save()

        # run the actual test
        response = client.get('/')
        assert response.status_code == 200

    def test_delete_view(self):
        # activate the client
        client = Client()

        # make a test user
        user = User.objects.create_user(username='testuser', password='testpass')
        client.force_login(user)

        # create the 2 posts
        p1 = Post(title = "title", body = "blank", published_date = timezone.now(), created_by = user)
        p1.save()
        
        # the seccond post uses the same title
        p2 = Post(title = "title", body = "blank", published_date = timezone.now(), created_by = user)
        p2.save()

        # save the id of the p2 post
        p1_id = p1.id

        # run the actual test
        response = client.get('/'+str(p1.id)+'/delete/')
        
        self.assertFalse(Post.objects.filter(id=p1.id).exists())