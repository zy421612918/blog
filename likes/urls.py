#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-6-9


from django.urls import path
from . import views


urlpatterns = [
    path('like_change', views.like_change, name='like_change')
]