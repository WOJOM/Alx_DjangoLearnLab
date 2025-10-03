
# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='password123')
        self.other = User.objects.create_user(username='bob', password='password123')
        self.post = Post.objects.create(title='Test', content='Body', author=self.user)

    def test_create_comment_requires_login(self):
        url = reverse('comment-create', kwargs={'post_pk': self.post.pk})
        resp = self.client.post(url, {'content': 'Nice post!'})
        self.assertNotEqual(resp.status_code, 200)
        self.client.login(username='alice', password='password123')
        resp = self.client.post(url, {'content': 'Nice post!'})
        self.assertEqual(resp.status_code, 302)  # redirect to post detail
        self.assertEqual(self.post.comments.count(), 1)

    def test_only_author_can_edit_or_delete(self):
        self.client.login(username='alice', password='password123')
        comment = Comment.objects.create(post=self.post, author=self.user, content='Hey')
        edit_url = reverse('comment-edit', kwargs={'pk': comment.pk})
        resp = self.client.get(edit_url)
        self.assertEqual(resp.status_code, 200)

        self.client.logout()
        self.client.login(username='bob', password='password123')
        resp = self.client.get(edit_url)
        # bob should be forbidden (or redirected)
        self.assertNotEqual(resp.status_code, 200)
