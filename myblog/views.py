#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-6-4
import string
import random
import time
from django.contrib.contenttypes.models import ContentType
from read_record.utils import get_sevendays_read,get_hot_data,yesterday_hot_data,get_7days_hot_date
from Blog.models import Blog
from django.shortcuts import render,redirect
from django.core.cache import cache
from django.views import View
from django.urls import reverse
from django.contrib import auth
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from user.form import ChangeNicknameForm,ForgetPwdForm
from user.models import Profile
from user.form import BindEmailCodeForm,ChangePwdForm
from utils.email_conf import changeEmailCode, changePassowrdCode
from django.contrib.auth.hashers import make_password




def home(request):
    blog_content_type =  ContentType.objects.get_for_model(Blog)
    read_list,date_list=get_sevendays_read(blog_content_type)
    # 获取7天热门博客的缓存数据
    # hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    # if hot_blogs_for_7_days is None:
    #     hot_blogs_for_7_days = get_7days_hot_date()
    #     cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)

    hot_blogs_for_7_days = get_7days_hot_date()
    context = {}
    context['read_list']=read_list # 返回一周的阅读数量列表
    context['date_list']=date_list # 返回一周的时间列表
    context['today_hot_data']=get_hot_data(content_type=blog_content_type) # 返回当日点击量最高的
    context['yesterday_hot_data']=yesterday_hot_data(content_type=blog_content_type) # 返回昨日点击量最高的
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    return render(request,'home.html', context)

class LoginView(View):
    """
    登录验证
    """
    def get(self,request):
        login_form = LoginForm()
        print('来自',request.get_full_path())

        context = {}
        context['login_form'] = login_form
        return render(request, 'login.html', context)

    def post(self,request):

        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)

            return redirect(request.GET.get('from', reverse('home')))
        else:
            context = {}
            context['login_form'] = login_form
            return render(request, 'login.html', context)


class RegisterView(View):
    def get(self,request):
        reg_form = RegForm()
        context = {}
        context['reg_form'] = reg_form
        return render(request, 'register.html', context)

    def post(self, request):
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']

            user =  User.objects.create_user(username, email, password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return  redirect(request.GET.get('from', reverse('home')))

        else:
            context = {}
            context['reg_form'] = reg_form
            return render(request, 'register.html', context)


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    print('modal')
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)

        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))



def user_info(request):
    context = {}
    return render(request, 'user_info.html', context)



def change_nickname(request):
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile,created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = ChangeNicknameForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back'] = request.GET.get('from', reverse('home'))
    return render(request,'forms.html',context)


def bind_email(request):
    if request.method == 'POST':
        form = BindEmailCodeForm(request.POST,request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = BindEmailCodeForm()
    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '确定'
    context['return_back'] = request.GET.get('from', reverse('home'))
    return render(request, 'bind_email.html', context)

def send_email_code(request):
    data = {}
    email = request.GET.get('email', '')
    print(email)
    request.session.get('send_code_time',0)
    if email!='':
        #生成验证码
        code= ''.join(random.sample(string.ascii_letters + string.digits,4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            print(request.GET.get('type'))
            if request.GET.get('type')=='changepassword':
                request.session['changepassword_code'] = code
                request.session['send_code_time'] = now
                changePassowrdCode(code=code,email=email)
                data['status'] = 'SUCCESS'
                return JsonResponse(data)
            elif request.GET.get('type') == 'resetpwd':
                request.session['resetpwd_code'] = code
                request.session['send_code_time'] = now
                changePassowrdCode(code=code, email=email)
                data['status'] = 'SUCCESS'

            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now
        #发送邮件
            changeEmailCode(code=code, email=email)
            return JsonResponse(data)

    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)



def rechange_pwd(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        form = ChangePwdForm(request.POST, request=request)
        if form.is_valid():
            password = form.cleaned_data['password2']
            request.user.password = make_password(password,hasher='default')
            request.user.save()
            return redirect(request.GET.get('from', reverse('home')))
    else:
        form = ChangePwdForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = '绑定密码(请先绑定邮箱再修改密码)'
    context['submit_text'] = '确定'
    context['return_back'] = request.GET.get('from', reverse('home'))
    return render(request, 'change_pwd.html', context)


def forget_pwd(request):
    redirect2 = reverse('home')

    if request.method == 'POST':
        form = ForgetPwdForm(request.POST, request=request)

        if form.is_valid():
            email = form.cleaned_data.get('email','').strip()
            new_password = form.cleaned_data.get('new_password','default').strip()
            print(email,new_password)
            user = User.objects.get(email=email)
            user.password = make_password(new_password,hasher='default')
            user.save()

            #清楚session
            return redirect(redirect2)
    else:
        form = ForgetPwdForm()

    context = {}
    context['form'] = form
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '确定'
    context['return_back'] = request.GET.get('from', reverse('home'))
    return render(request, 'for-getpwd.html', context)
