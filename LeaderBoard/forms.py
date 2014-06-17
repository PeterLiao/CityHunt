__author__ = 'peter_c_liao'

from django import forms


class PostForm(forms.Form):
    post_text = forms.CharField(max_length=200)
    city_id = forms.IntegerField()
    user_id = forms.IntegerField()


class CommentForm(forms.Form):
    comment_text = forms.CharField(max_length=200)
    post_id = forms.IntegerField()
    user_id = forms.IntegerField()


class PostLikeForm(forms.Form):
    post_id = forms.IntegerField()
    user_id = forms.IntegerField()


class UserForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
    user_id = forms.IntegerField()