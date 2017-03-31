# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models


class CityDict(models.Model):
    """城市信息"""
    name = models.CharField(max_length=20, verbose_name=u'城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    description = models.CharField(max_length=200, verbose_name=u'描述')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name


class CourseOrg(models.Model):
    """课程所属机构"""
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    description = models.TextField(verbose_name=u'机构描述')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    favor_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'封面图', max_length=100)
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    """讲师信息"""
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    name = models.CharField(max_length=50, verbose_name=u'教师姓名')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'职位')
    teach_feature = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    favor_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

