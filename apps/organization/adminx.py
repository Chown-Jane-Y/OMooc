# coding: utf-8
__author__ = 'gocjy'
__date__ = '2017/3/31 15:43'

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'description', 'add_time']
    search_fields = ['name']
    list_filter = ['name', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'description', 'click_nums', 'favor_nums', 'address', 'add_time']
    search_fields = ['name', 'address']
    list_filter = ['name', 'address', 'add_time', 'favor_nums']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'click_nums', 'favor_nums', 'add_time']
    search_fields = ['org', 'name', 'work_company']
    list_filter = ['org', 'name', 'work_company', 'add_time', 'favor_nums']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)