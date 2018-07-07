#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-6-8

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from captcha.fields import CaptchaField



class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名',widget=forms.TextInput(attrs={
            'class':'form-control', 'placeholder':'请输入用户名或者邮箱'
        })
    )
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    captcha = CaptchaField(error_messages={'invalid': '验证码错误啊'},label='验证码：')
    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email,password=password)
        if not user:
            raise forms.ValidationError('用户名或者密码错误')
        else:
            self.cleaned_data['user']=user

        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=20,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入3-30位用户名'}))
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='再输入一次密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control', 'placeholder': '再输入一次密码'}))
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'},label='验证码：')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户已经存在')

        return username


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean(self):
        cleaned_data = self.cleaned_data
        pwd = cleaned_data['password']

        pwd2 = cleaned_data['password']
        if pwd != pwd2:
            raise forms.ValidationError('二次输入密码不匹配')
        return cleaned_data  # 注意此处一定要return clean_data,否则会报错



