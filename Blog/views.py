from django.shortcuts import render,render_to_response,get_object_or_404,HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count,Q
from Blog import models
from django.contrib.contenttypes.models import ContentType
from read_record.models import ReadNum
from read_record.utils import check_read_record
from comment.models import Comment
from comment.forms import CommentForm
from myblog.forms import LoginForm


def blog_list(request):
    """
    全局博客列表页
    :param request:
    :return:
    """
    all_blog = models.Blog.objects.all().order_by('-created_time')
    blog_dates = models.Blog.objects.extra(
        select={
            'ctime': "date_format(created_time,'%%Y-%%m')"}).order_by('ctime').values('ctime').annotate(ct=Count('id'))
    blog_types = models.BlogType.objects.all()
    # 对博客列表进行分页
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(all_blog, 5, request=request)
    blogs = p.page(page)
    return render(request,'blog_list.html', {'blogs': blogs, 'blog_types': blog_types, 'blog_dates': blog_dates})


def blog_detail(request, blog_pk):
    """
    博客详情页
    :param request:
    :param blog_pk:
    :return:
    """

    blog = get_object_or_404(models.Blog, id=blog_pk)

    read_cookie_key = check_read_record(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk,parent=None)
    context = {}
    context['previous_blog'] = models.Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = models.Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    context['comments'] = comments
    context['login_form'] = LoginForm()

    context['coment_form'] = CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog_pk,'reply_comment_id':0})
    response = render(request, 'blog_detail.html', context)  # 响应
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response


def blogs_with_type(request, blog_type_pk):
    """
    博客分类列表页
    :param request:
    :param blog_type_pk:
    :return:
    """
    blog_type = get_object_or_404(models.BlogType, pk=blog_type_pk)

    blog_types = models.BlogType.objects.all()

    all_blog = models.Blog.objects.filter(blog_type=blog_type)
    blog_dates = models.Blog.objects.extra(
        select={'ctime': "date_format(created_time,'%%Y-%%m')"}).values('ctime').annotate(ct=Count('id'))
    # 对博客列表进行分页
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(all_blog, 5, request=request)
    blogs = p.page(page)
    return render(request,'blogs_with_type.html',
                              {'blogs': blogs, 'blog_types': blog_types, 'blog_dates': blog_dates})


def blogs_with_date(request, val):
    """
    时间分类博客列表页
    :param request:
    :param val:
    :return:
    """
    blogs = models.Blog.objects.extra(
        where=["date_format(created_time,'%%Y-%%m')=%s"], params=[val, ]
    )
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(blogs, 5, request=request)
    blogs = p.page(page)
    blog_types = models.BlogType.objects.all()
    blog_dates = models.Blog.objects.extra(
        select={'ctime': "date_format(created_time,'%%Y-%%m')"}).values('ctime').annotate(ct=Count('id'))
    context = {}
    context['blogs'] = blogs
    context['blogs_with_date'] = blogs_with_date
    context['blog_types'] = blog_types
    context['blog_dates'] = blog_dates
    return render(request,'blogs_with_date.html', context)