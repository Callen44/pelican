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
        response = client.get('/'+str(p2.id)+'/update/')
        assert response.status_code == 200

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
        print('/'+str(p1.id)+'/delete/')
        response = client.get('/'+str(p1.id)+'/delete/')
        
        self.assertFalse(Post.objects.filter(id=p1.id).exists())