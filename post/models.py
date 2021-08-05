from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.author.id, filename)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_directory_path)
    caption = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.caption)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')

    def __str__(self):
        return "{0} likes {1}".format(self.user.username,self.post.caption)

class Follow(models.Model):
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='master')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return "{0} follows {1}".format(self.follower, self.master)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    content = models.TextField(max_length=200)
    likes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)
