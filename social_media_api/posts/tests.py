from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class PostsCommentsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass')
        self.user2 = User.objects.create_user(username='bob', password='pass')
        self.post = Post.objects.create(author=self.user, title='Hello', content='World')

    def test_create_post_requires_auth(self):
        url = reverse('post-list')
        data = {'title': 'New', 'content': 'Content'}
        resp = self.client.post(url, data)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.client.force_authenticate(self.user)
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_post_list_and_search(self):
        url = reverse('post-list')
        resp = self.client.get(url, {'search': 'Hello'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(any(item['title'] == 'Hello' for item in resp.data['results']))

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {'post': self.post.id, 'content': 'Nice post'}
        self.client.force_authenticate(self.user2)
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.post.comments.count(), 1)

    def test_comment_edit_by_owner_only(self):
        comment = Comment.objects.create(post=self.post, author=self.user2, content='c')
        url = reverse('comment-detail', args=[comment.id])
        self.client.force_authenticate(self.user)
        resp = self.client.patch(url, {'content': 'x'})
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED))
        self.client.force_authenticate(self.user2)
        resp = self.client.patch(url, {'content': 'edited'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
