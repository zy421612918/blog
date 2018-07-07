from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone


class ReadNum(models.Model):
    """
    阅读信息
    """
    read_num = models.IntegerField(default=0, verbose_name='阅读数量')
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, verbose_name='类型')
    object_id = models.PositiveSmallIntegerField()
    Content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读统计'
        verbose_name_plural = verbose_name


class ReadCount():

    def get_read_num(self):
        """
        返回对应阅读属性
        :return:
        """
        ct = ContentType.objects.get_for_model(self)
        try:
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

class ReadDetail(models.Model):
    """
    用于统计时间段访问
    """
    date = models.DateField(default=timezone.now)
    read_num = models.IntegerField(default=0, verbose_name='阅读数量')
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING, verbose_name='类型')
    object_id = models.PositiveSmallIntegerField()
    Content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读详细'
        verbose_name_plural = verbose_name


