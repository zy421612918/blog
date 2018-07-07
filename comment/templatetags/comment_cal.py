#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-6-8
from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
register = template.Library()


@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.id).count()