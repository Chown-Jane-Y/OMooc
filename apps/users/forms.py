# coding: utf-8
__author__ = 'gocjy'
__date__ = '2017/4/1 11:18'

from django import forms
from captcha.fields import CaptchaField

"""
html中表单里的name必须和这里的变量名相同，一一对应，否则不会识别
"""


# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True)                       # required=True不允许为空
    password = forms.CharField(required=True, min_length=6)          # 最小长度为6，不满足条件则不会查询数据库


# 注册表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


# 找回密码表单
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


# 忘记密码-重置密码
class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)
