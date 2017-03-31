# coding: utf-8
__author__ = 'gocjy'
__date__ = '2017/3/31 15:04'

from .models import Course, Lesson, Video, CourseResource

import xadmin


class CourseAdmin(object):
    list_display = ['name', 'degree', 'students', 'favor_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'description', 'detail', 'degree', 'learn_time', 'students', 'favor_nums', 'image', 'click_nums', 'add_time']
    list_filter = ['name', 'description', 'detail', 'degree', 'learn_time', 'students', 'favor_nums', 'image', 'click_nums', 'add_time']


class LessonAdmin(object):
    list_display = ['name', 'course', 'add_time']
    search_fields = ['name', 'course']
    list_filter = ['name', 'course__name', 'add_time']


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'lesson', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['name', 'course', 'download', 'add_time']
    search_fields = ['name', 'course', 'download']
    list_filter = ['name', 'course', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)