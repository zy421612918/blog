#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-6-8

from django.urls import path
from . import views


urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment')
]
