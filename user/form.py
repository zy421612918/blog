#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-6-11

from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User


class ChangePwdForm(forms.Form):
    password1= forms.CharField(
        label='新密码', max_length=20, min_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入6-20位的新密码'}
         ))
    password2 = forms.CharField(
        label='确认密码', max_length=20, min_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}
         ))


    verification = forms.CharField(label='验证码',required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '请输入绑定的邮箱验证码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangePwdForm, self).__init__(*args, **kwargs)

    def clean(self):
        '''
        判断用户是否登录
        :return:
        '''
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户未登录')
        cleaned_data = self.cleaned_data

        code = self.request.session.get('changepassword_code', '')
        verification = self.cleaned_data.get('verification', '')
        pwd = cleaned_data['password1'].lower()
        pwd2 = cleaned_data['password2'].lower()
        if pwd != pwd2:
            raise forms.ValidationError('二次输入密码不匹配')
        elif not (code != '' and code == verification):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data


class ChangeNicknameForm(forms.Form):

    nickname_new = forms.CharField(label='新的昵称',max_length=20,min_length=2,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入2-20位昵称'}
                                                      ))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        '''
        判断用户是否登录
        :return:
        '''
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户未登录')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new','').strip()
        if nickname_new =='':
            raise ValidationError('新的昵称不能为空')
        return nickname_new


class BindEmailCodeForm(forms.Form):
    email = forms.EmailField(label='新的邮箱',
                             widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '请输入正确的邮箱'}))
    verification = forms.CharField(label='验证码',required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '点击发送验证码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailCodeForm, self).__init__(*args, **kwargs)

    def clean(self):
        '''
        判断用户是否登录
        :return:
        '''
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户未登录')
        if self.request.user.email !='':
            raise forms.ValidationError('你已经绑定邮箱')

        code = self.request.session.get('bind_email_code','')
        verification = self.cleaned_data.get('verification', '')
        print(code,verification)

        if not(code!='' and code== verification ):
            raise forms.ValidationError('验证码不正确')


        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():

            raise forms.ValidationError('该邮箱已经绑定')

        return email


    def clean_verification(self):
        verification = self.cleaned_data.get('verification', '').strip()
        if verification =='':
            raise forms.ValidationError('验证码不能为空')

        return verification


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(max_length=50, label='邮箱',required=False,
                               widget=forms.TextInput(
                                   attrs={'class':'form-control','placeholder':'请输入绑定的邮箱'}
                               ))
    verification = forms.CharField(label='验证码', required=False,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': '请输入绑定的邮箱验证码'}))
    new_password = forms.CharField(label='新密码', required=False,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': '请输入新的密码'}))
    def __init__(self,*args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgetPwdForm,self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email = email).exists():
            raise forms.ValidationError('邮箱不存在！')
        return email

    def clean_verification(self):
        verification_code = self.cleaned_data.get('verification','').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        code = self.request.session.get('resetpwd_code','')
        print(code)
        verification_code = self.cleaned_data.get('verification','')
        print(verification_code)
        if not(code !='',code == verification_code ):
            raise forms.ValidationError('验证码不正确')

        return verification_code









