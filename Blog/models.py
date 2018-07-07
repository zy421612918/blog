from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from read_record.models import ReadNum,ReadCount,ReadDetail



class BlogType(models.Model):
    """
    博客类型
    """
    type_name = models.CharField(max_length=15, verbose_name='博客类型')

    def __str__(self):
        return self.type_name

    def get_type_nums(self):
        return self.blog_set.count()

    class Meta:
        verbose_name = '博客类型'
        verbose_name_plural = verbose_name


class Blog(models.Model, ReadCount):
    """
    博客信息
    """
    title = models.CharField(max_length=30, verbose_name='博客标题')
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING, verbose_name='博客类型')
    content = RichTextUploadingField(verbose_name='博客内容')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='博客作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_update_time = models.DateTimeField(auto_now_add=True, verbose_name='最后修改时间')
    read_details = GenericRelation(ReadDetail)


    def __str__(self):
        return self.title
    class Meta:
        verbose_name = '博客信息'
        verbose_name_plural = verbose_name


