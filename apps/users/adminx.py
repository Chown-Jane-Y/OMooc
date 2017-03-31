# coding: utf-8
__author__ = 'gocjy'
__date__ = '2017/3/31 14:33'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord
from .models import Banner


class BaseSetting(object):
    enable_themes = True                # 允许配置主题
    use_bootswatch = True               # 加入主题


class GlobalSettings(object):
    """全局配置"""
    site_title = 'OMooc后台管理系统'      # 后台网站标题
    site_footer = 'OMooc'                 # 网站底部
    menu_style = 'accordion'              # 导航栏样式，可展开


class EmailVerifyRecordAdmin(object):  # 要使用xadmin的register，只能继承object类
    list_display = ['code', 'email', 'send_type', 'send_time']  # 后台管理页面中默认显示的列
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index', 'add_time']
    list_filter = ['title', 'image', 'url', 'index']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)