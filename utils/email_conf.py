#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-6-12

from django.core.mail import send_mail



def changePassowrdCode(code, email):
    send_mail(
        '修改密码',
        '验证码:%s' % code,
        '421612918@qq.com',
        [email],
        fail_silently=False
    )




def changeEmailCode(code,email):
    '''发送更换邮箱的功能'''
    send_mail(
        '绑定邮箱',
        '验证码:%s' % code,
        '421612918@qq.com',
        [email],
        fail_silently=False
    )