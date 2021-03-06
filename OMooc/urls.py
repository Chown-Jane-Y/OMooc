# coding: utf-8
"""OMooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin

from django.conf.urls import url, include
from django.views.generic import TemplateView    # 处理静态文件
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPasswordView, ResetPasswordHtmlView, ResetPasswordView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),  # as_view()括号不能少
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls'), name='captcha'),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),   # 把active/后面字符串提取出来放到active_code中
    url(r'^forget/$', ForgetPasswordView.as_view(), name='forget_password'),
    url(r'^reset/(?P<active_code>.*)/$', ResetPasswordHtmlView.as_view(), name='reset_password_html'),
    url(r'^resetpwd/$', ResetPasswordView.as_view(), name='reset_password'),    # 注意和上面的url区分
]
