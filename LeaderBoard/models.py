from django.db import models
from LeaderBoard.common import *
# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    fb_id = models.IntegerField(primary_key=True)
    pub_date = models.DateTimeField('date published')


class Post(models.Model):
    user = models.ForeignKey(User)
    post_text = models.CharField(max_length=200)
    city = models.ForeignKey(City)
    pub_date = models.DateTimeField('date published')

    def get_formatted_timedelta(self):
        return get_formatted_timedelta_by_now(self.pub_date)

    pub_date_str = property(get_formatted_timedelta)


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    comment_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def get_formatted_timedelta(self):
        return get_formatted_timedelta_by_now(self.pub_date)

    pub_date_str = property(get_formatted_timedelta)


class PostLike(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    pub_date = models.DateTimeField('date published')


class CommentLike(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    pub_date = models.DateTimeField('date published')
