from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

class Comment(models.Model):
    """
    评论功能
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, verbose_name='类型')
    object_id = models.PositiveSmallIntegerField(verbose_name='关联对象')
    #关联对象
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True)
    user =models.ForeignKey(User,on_delete=models.DO_NOTHING, verbose_name='用户')
    parent = models.ForeignKey('self',null=True,related_name='parent_comment', on_delete=models.DO_NOTHING, verbose_name='父级对象')
    root = models.ForeignKey('self',null=True,related_name='root_comment', on_delete=models.DO_NOTHING)

    reply_to = models.ForeignKey(User,null=True, on_delete=models.DO_NOTHING, verbose_name='回复的对象',related_name='replies')

    class Meta:
        verbose_name = '评论记录'
        verbose_name_plural = verbose_name






