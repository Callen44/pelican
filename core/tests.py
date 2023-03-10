import datetime
import os

from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .views import update
from .models import Post, Like


class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.force_login(self.user)

    def test_update_view(self):
        posts = [Post.objects.create(title='title', body='blank', published_date=timezone.now(), created_by=self.user) for _ in range(2)]
        p1 = posts[0]

        response = self.client.get(f'/{p1.id}/update/')
        csrf_token = response.cookies['csrftoken'].value

        data = {
            'title': 'I am a mongoose',
            'body': 'it is true',
            'csrfmiddlewaretoken': csrf_token,
        }
        response = self.client.post(f'/{p1.id}/update/', data=data)

        self.assertEqual(response.status_code, 302)

        p1.refresh_from_db()
        self.assertEqual(p1.title, 'I am a mongoose')

    def test_index_view(self):
        posts = [Post.objects.create(title='title', body='blank', published_date=timezone.now(), created_by=self.user) for _ in range(2)]

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_delete_view(self):
        posts = [Post.objects.create(title='title', body='blank', published_date=timezone.now(), created_by=self.user) for _ in range(2)]
        p1 = posts[0]

        response = self.client.get(f'/{p1.id}/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=p1.id).exists())