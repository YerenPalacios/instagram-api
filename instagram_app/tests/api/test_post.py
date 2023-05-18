from django.urls import reverse
from django_dynamic_fixture import G
from rest_framework.test import APITestCase

from instagram_app.models import User, Post, Follow, Comment, Like, Save
from instagram_app.views.post import PostsView


class PostTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(PostsView.name)
        cls.user: User = G(User)
        cls.user_2: User = G(User)
        cls.user_3: User = G(User)
        cls.post_1 = G(Post, user=cls.user_2)
        cls.post_2 = G(Post)
        cls.post_3 = G(Post)
        cls.post_4 = G(Post)
        cls.post_5 = G(Post)

        G(Follow, follower=cls.user, following=cls.user_2)

        G(Comment, user=cls.user_2, text="comment1", post=cls.post_1)
        G(Comment, user=cls.user, text="comment2", post=cls.post_1)
        G(Comment, user=cls.user_3, text="comment3", post=cls.post_1)

        G(Like, user=cls.user, post=cls.post_1)
        G(Like, user=cls.user_3, post=cls.post_1)

        G(Save, user=cls.user, post=cls.post_5)

    def test_get_posts_for_not_authenticated_user(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 5)
        self.assertEqual(res.data[0]["id"], self.post_5.id)
        self.assertEqual(res.data[1]["id"], self.post_4.id)
        self.assertEqual(res.data[2]["id"], self.post_3.id)
        self.assertEqual(res.data[3]["id"], self.post_2.id)
        self.assertEqual(res.data[4]["id"], self.post_1.id)

        self.assertEqual(res.data[4]["last_owner_comment"], "comment1")
        self.assertEqual(res.data[4]["comments_count"], 3)
        self.assertEqual(res.data[4]["likes_count"], 2)

        self.assertIsNone(res.data[0]["is_liked"])
        self.assertIsNone(res.data[0]["is_saved"])

    def test_get_posts_for_authenticated_user(self):
        self.client.force_authenticate(self.user)
        res = self.client.get(self.url, data={"priority": True})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 5)
        self.assertEqual(res.data[0]["id"], self.post_1.id)
        self.assertEqual(res.data[1]["id"], self.post_5.id)
        self.assertEqual(res.data[2]["id"], self.post_4.id)
        self.assertEqual(res.data[3]["id"], self.post_3.id)
        self.assertEqual(res.data[4]["id"], self.post_2.id)

        self.assertEqual(res.data[0]["last_owner_comment"], "comment1")
        self.assertEqual(res.data[0]["comments_count"], 3)
        self.assertEqual(res.data[0]["likes_count"], 2)
        self.assertEqual(res.data[1]["comments_count"], 0)
        self.assertEqual(res.data[1]["likes_count"], 0)

        self.assertEqual(res.data[0]["is_liked"], True)
        self.assertEqual(res.data[0]["is_saved"], False)

        self.assertEqual(res.data[1]["is_liked"], False)
        self.assertEqual(res.data[1]["is_saved"], True)

    # TODO: validate user fields in test
