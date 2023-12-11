from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.fields.related import ForeignKey

from instagram_app.dto.user import UserDTO


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('Email must be provided')

        email = self.normalize_email(email)
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, name=name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='uploads', null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=10, default='#ff2f00')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.email}: {self.username}'

    def to_dto(self) -> UserDTO:
        return UserDTO(
            id=self.id,
            name=self.name,
            username=self.username,
            email=self.email,
            phone=self.phone,
            image=self.image.url if self.image else '',
            is_active=self.is_active,
            is_staff=self.is_staff,
            description=self.description,
            color=self.color,
            is_following=getattr(self, "following", None)
        )


class Post(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)


class Files(models.Model):
    file = models.FileField(upload_to='uploads/posts', blank=True, null=True)
    post = ForeignKey(Post, related_name='files', on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'Comment', blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    send_to = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="send_to")
    created_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='likes',
        on_delete=models.CASCADE, blank=True, null=True
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, blank=True, null=True)
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, blank=True, null=True)


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='saves',
        on_delete=models.CASCADE, blank=True, null=True
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, blank=True, null=True)


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'], name='unique follow')
        ]

    def __str__(self):
        return f'{self.follower} following {self.following}'


class PublicChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    user = models.ManyToManyField(get_user_model(), blank=True)

    def connect_user(self, user):
        is_user_added = False
        if user not in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = False
        else:
            is_user_added = False
        return is_user_added

    def disconnet_user(self, user):
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        return f'PublicChatRoom-{self.id}'


class PublicChatRoomMessageManager(models.Manager):
    def by_room(self, room):
        return self.model.objects.filter(room=room).order_by('-timestamp')


class PublicChatRoomMessage(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.content
