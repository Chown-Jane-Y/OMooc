# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """用户信息"""
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default=u'游客学员')          # 昵称，默认 游客学员
    birthday = models.DateField(verbose_name=u'生日', null=True)                                   # 生日，可为空
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')), default='female', verbose_name=u'性别')     # 性别，可选，默认女
    address = models.CharField(max_length=100, verbose_name=u'地址', default=u'')                   # 地址，默认为空
    mobile = models.CharField(max_length=11, verbose_name=u'手机', null=True)                      # 手机，可为空
    image = models.ImageField(upload_to='image/%Y/%m', default=u'image/default.png', max_length=100, verbose_name=u'头像') # 头像，默认default.png

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    """邮箱验证"""
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=(('register', u'注册'), ('forget', u'找回密码')), max_length=10, verbose_name=u'验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')                 # 注意now后面不要跟括号，否则会是model创建时的时间

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return u'验证码【{0}】 发送至邮箱【{1}】验证码类型【{2}】'.format(self.code, self.email, self.send_type)

class Banner(models.Model):
    """轮播图"""
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u'轮播图', max_length=100)
    url = models.CharField(max_length=200, verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
