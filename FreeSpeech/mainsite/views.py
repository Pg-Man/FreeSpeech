from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post,Mood
from django.template.loader import get_template
from django.template import RequestContext,Context
from . import models,forms
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(request,pid=None,del_pass=None):
    template = get_template('index.html')
    posts = Post.objects.filter(enabled=True).order_by('-pub_time')[:30]#filter过滤初enabled字段是True的数据项
    #然后再order_by对pub_time进行排序（增减），最后[:30]是只取出最新的30条信息
    moods = Mood.objects.all()

    try:
        user_id = request.GET['user_id']
        user_pass = request.GET['user_pass']
        user_post = request.GET['user_post']
        user_mood = request.GET['mood']
    except:
        user_id = None
        message = '如果要张贴信息，那么每一个字段都要填......'
    if del_pass and pid:
        try:
            post = Post.objects.get(id=pid)
        except:
            post = None
        if post:
            if post.del_pass == del_pass:
                post.delete()
                message = "数据删除成功"
            else:
                message = "密码错误"

    elif user_id != None:
        mood = Mood.objects.get(status=user_mood)
        post = Post.objects.create(mood=mood, nickname=user_id,del_pass=user_pass,message=user_post)
        post.save()
        message = '成功存储！请记住您的编辑密码[{}]!，信息须经审查后才会显示。'.format(user_pass)

    html =template.render(locals())
    return HttpResponse(html)

def listing(request):
    template = get_template('listing.html')
    posts = Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods = Mood.objects.all()

    html = template.render(locals())
    return HttpResponse(html)

def posting(request):
    template = get_template('posting.html')
    moods = Mood.objects.all()
    message = '如果要张贴信息，那么每一个字段都要填写......'
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)
    return HttpResponse(html)

def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message = "感谢您的来信"
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']
            msg = '<a href="哈哈哈" target="_blank">点击激活</a>'
            mail_body = u'''
            网友姓名:{}
            居住城市:{}
            是否在学:{}
            反应意见如下:
            {}
            '''.format(user_name,user_city,user_school,user_message)
            send_mail('来自【不吐不快】网站的网友意见',mail_body,user_email,['ypjngup@163.com'])
        else:
            message = "请检查您输入的信息是否正确"
    else:
        form = forms.ContactForm()
    template = get_template('contact.html')
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)
    return HttpResponse(html)

def post2db(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            message = '您的信息已存储，要等管理员启用后才看得到'
            post_form.save()
            return HttpResponseRedirect('/list/')
        else:
            message = '如果要张贴信息，那么每一个字段都要填...'
    else:
        post_form = forms.PostForm()
    template = get_template('post2db.html')
    post_form = forms.PostForm()
    moods = Mood.objects.all()
    message = '如果要张贴信息，那么每一个字段都要填...'
    request_context = RequestContext(request)
    request_context.push(locals())
    html = template.render(request_context)

    return HttpResponse(html)