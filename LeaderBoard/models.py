from django.db import models
from LeaderBoard.common import get_formatted_timedelta_by_now
# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=60)
    pub_date = models.DateTimeField('date published')


class User(models.Model):
    name = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    email = models.EmailField()
    fb_id = models.IntegerField(primary_key=True)
    pub_date = models.DateTimeField('date published')


class Post(models.Model):
    user = models.ForeignKey(User)
    post_text = models.CharField(max_length=60)
    post_title = models.CharField(max_length=30)
    city = models.ForeignKey(City)
    pub_date = models.DateTimeField('date published')

    def get_formatted_timedelta(self):
        return get_formatted_timedelta_by_now(self.pub_date)

    def get_like_count(self):
        return PostLike.objects.filter(post=self).count()

    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()

    pub_date_str = property(get_formatted_timedelta)
    like_count = property(get_like_count)
    comment_count = property(get_comment_count)


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    comment_text = models.CharField(max_length=60)
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
