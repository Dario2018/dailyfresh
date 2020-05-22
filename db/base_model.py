from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    '''所有模型的抽象基类'''
    create_date = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    update_date = models.DateTimeField(default=timezone.now, verbose_name="更新时间")
    is_delete = models.BooleanField(default=True, verbose_name="删除标记")

    class Meta:
        # 说明是一个抽象模型类
        abstract = True
