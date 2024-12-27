# -*- coding: utf-8 -*-
# author:laoseng(QQ:1572665580),feilong(hhr66@qq.com)
# create:2018-09
# ORM 基础类

from django.db import models


class BaseModel(models.Model):
    '''
       基础表(抽象类)
    '''
    id = models.AutoField(primary_key=True, verbose_name='主键ID')
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='更新时间', auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-id']
