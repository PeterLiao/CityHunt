from django.shortcuts import render
import datetime
import json
from datetime import date, timedelta
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from LeaderBoard.forms import *
from LeaderBoard.common import *
from LeaderBoard.models import *


# Create your views here.
def add_user(request):
    result = 'fail'
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = User(name=form.cleaned_data['name'],
                        fb_id=form.cleaned_data['user_id'],
                        email=form.cleaned_data['email'],
                        pub_date=get_utc_now())
            user.save()
            result = 'ok'
    response_data = {}
    response_data['result'] = result
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def add_post_page(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            city = City.objects.filter(id=form.cleaned_data['city_id'])[0]
            user = User.objects.filter(fb_id=form.cleaned_data['user_id'])[0]
            post = Post(post_text=form.cleaned_data['post_text'], post_title=form.cleaned_data['post_title'], city=city, user=user, pub_date=get_utc_now())
            post.save()
        else:
            print form.errors
    return HttpResponseRedirect('/hottest/')


def add_comment_page(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = Post.objects.filter(id=form.cleaned_data['post_id'])[0]
            user = User.objects.filter(fb_id=form.cleaned_data['user_id'])[0]
            comment = Comment(comment_text=form.cleaned_data['comment_text'], post=post, user=user, pub_date=get_utc_now())
            comment.save()
        else:
            print form.errors
    return HttpResponseRedirect("/hottest/%d" % post.id)


def add_post_like_page(request):
    result = 'fail'
    if request.method == 'POST':
        form = PostLikeForm(request.POST)
        if form.is_valid():
            post = Post.objects.filter(id=form.cleaned_data['post_id'])[0]
            user = User.objects.filter(fb_id=form.cleaned_data['user_id'])[0]
            post_like = PostLike.objects.filter(post=post, user=user)
            if post_like.count() == 0:
                post_like = PostLike(post=post, user=user, pub_date=get_utc_now())
                post_like.save()
                result = 'like'
            elif post_like.count() == 1:
                PostLike.objects.filter(post=post, user=user).delete()
                result = 'not_like'
    response_data = {}
    response_data['result'] = result
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def post_detail_page(request, post_id):
    try:
        user_id = 0
        if 'user_id' in request.COOKIES:
            user_id = request.COOKIES.get('user_id')
        post = Post.objects.filter(id=post_id)[0]
        comment_list = Comment.objects.filter(post=post)
        like_list = PostLike.objects.filter(post=post)
        logged_user = User.objects.filter(fb_id=user_id)
        liked = PostLike.objects.filter(post=post, user=logged_user).count()
        return render_to_response("detail.html", {"current_page": "hottest",
                                                  "post_obj": post,
                                                  "comment_list": comment_list,
                                                  "like_list": like_list,
                                                  "liked": liked,
                                                  "user_form": UserForm(),
                                                  "post_like_form": PostLikeForm()},
                                                  context_instance = RequestContext(request))
    except IndexError:
        raise Http404



def get_post_data_by_date(start_date, end_date):
    data_list = []
    post_list = Post.objects.filter(pub_date__gte=start_date, pub_date__lte=end_date)
    post_list = sorted(post_list, key=lambda x: x.like_count, reverse=True)
    for post in post_list:
        data_list.append({"post": post, "liked": 0})
    return data_list


def get_post_data_by_date_ex(start_date, end_date, user_id):
    data_list = []
    post_list = Post.objects.filter(pub_date__gte=start_date, pub_date__lte=end_date)
    post_list = sorted(post_list, key=lambda x: x.like_count, reverse=True)
    logged_user = User.objects.filter(fb_id=user_id)
    for post in post_list:
        liked = PostLike.objects.filter(post=post, user=logged_user).count()
        data_list.append({"post": post, "liked": liked})
    return data_list


def hottest_page(request):
    user_id = 0
    if 'user_id' in request.COOKIES:
        user_id = request.COOKIES.get('user_id')

    days_ago = 0
    while True:
        post_list_in_today = get_post_data_by_date_ex(datetime.date.today()-timedelta(days_ago),
                                                      datetime.date.today()+timedelta(1)-timedelta(days_ago),
                                                      user_id)
        if len(post_list_in_today) > 0 or days_ago >= 30:
            break
        else:
            days_ago += 1

    while True:
        post_list_in_yesterday = get_post_data_by_date_ex(datetime.date.today()-timedelta(1)-timedelta(days_ago),
                                                        datetime.date.today()-timedelta(days_ago),
                                                        user_id)
        if len(post_list_in_yesterday) > 0 or days_ago >= 30:
            break
        else:
            days_ago += 1

    while True:
        post_list_in_two_days_ago = get_post_data_by_date_ex(datetime.date.today()-timedelta(2)-timedelta(days_ago),
                                                            datetime.date.today()-timedelta(1)-timedelta(days_ago),
                                                            user_id)
        if len(post_list_in_two_days_ago) > 0 or days_ago >= 30:
            break
        else:
            days_ago += 1

    while True:
        post_list_in_three_days_ago = get_post_data_by_date_ex(datetime.date.today()-timedelta(3)-timedelta(days_ago),
                                                            datetime.date.today()-timedelta(2)-timedelta(days_ago),
                                                            user_id)
        if len(post_list_in_three_days_ago) > 0 or days_ago >= 30:
            break
        else:
            days_ago += 1

    return render_to_response("hottest.html",
                              {"current_page": "hottest",
                               "today": get_formatted_date(datetime.date.today()),
                               "today_list": post_list_in_today,
                               "yesterday": get_formatted_date(datetime.date.today()-timedelta(1)),
                               "yesterday_list": post_list_in_yesterday,
                               "two_days_ago_list": post_list_in_two_days_ago,
                               "two_days_ago": get_formatted_date(datetime.date.today()-timedelta(2)),
                               "three_days_ago_list": post_list_in_three_days_ago,
                               "three_days_ago": get_formatted_date(datetime.date.today()-timedelta(3)),
                               "user_form": UserForm(),
                               "post_like_form": PostLikeForm()},
                               context_instance = RequestContext(request))



def hottest_logged_page(request, user_id):
    post_list_in_today = get_post_data_by_date_ex(datetime.date.today(), datetime.date.today()+timedelta(1), user_id)
    post_list_in_yesterday = get_post_data_by_date_ex(datetime.date.today()-timedelta(1), datetime.date.today(), user_id)
    return render_to_response("hottest.html",
                              {"current_page": "hottest",
                               "today": get_formatted_date(datetime.date.today()),
                               "today_list": post_list_in_today,
                               "yesterday": get_formatted_date(datetime.date.today()-timedelta(1)),
                               "yesterday_list": post_list_in_yesterday,
                               "user_form": UserForm(),
                               "post_like_form": PostLikeForm()},
                               context_instance = RequestContext(request))


def about_page(request):
    return render_to_response("about.html", {'current_page': 'about'})


def login_page(request):
    return render_to_response("login.html", {'current_page': 'login'})


def fb_page(request):
    return render_to_response("fb.html")