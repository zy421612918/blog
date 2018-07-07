#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Zhangye"
# Date: 18-6-6
import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail
from django.utils import timezone
from django.db.models import Sum
from Blog.models import Blog


def check_read_record(request,obj):
    """
    检查是否阅读过
    :param request:
    :param obj: blog对象
    :return: cookie标记
    """
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read'%(ct.model, obj.pk)   #  blog_35_read
    if not request.COOKIES.get(key):
        # 总阅读数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当日计数+1
        date = timezone.now().date()
        readDetail,created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num+=1
        readDetail.save()
    return key

def get_sevendays_read(content_type):
    today = timezone.now().date()
    read_list=[]
    date_list=[]
    print(today)
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        date_list.append(date.strftime('%m/%d'))

        read_details=ReadDetail.objects.filter(content_type=content_type, date=date)

        res = read_details.aggregate(read_nums=Sum('read_num'))
        read_list.append(res['read_nums'] or 0)

    return read_list,date_list


def get_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:3]


def yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today- datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:3]

def get_7days_hot_date():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today,
                                read_details__date__gte=date).\
        values('id','title')\
        .annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return blogs[:7]



