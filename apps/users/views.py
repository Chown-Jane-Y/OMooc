# coding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from users.models import UserProfile
from users.forms import LoginForm, RegisterForm
from util.email_send import send_register_email


class CustomBackend(ModelBackend):                  # 重载authenticate函数，可以通过邮箱验证登录
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))     # 不查询密码，因为密码存储是密文，前端传回是明文，无法匹配
            if user.check_password(password):                                  # Q是数据库的或操作，用username或email查询
                print 'check success'
                return user
        except Exception as e:
            return None


class LoginView(View):                              # 继承Django自己的View，重载View类中的函数，减少自己编写逻辑代码
    def get(self, request):                         # django会自动判断request.method，如果是get，则调用get()函数
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():               # 判断表单里提交的数据是否合法(在forms.py里设置)
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)         # 用户认证，判断用户名密码是否匹配，匹配成功返回一个对象，否则返回None
            if user is not None:                            # 如果不为空，则登录这个用户
                login(request, user)                        # 根据用户信息生成一个session
                return render(request, 'index.html')
            else:                                           # (查询数据库之后)用户名密码出错返回错误msg
                return render(request, 'login.html', {'msg': '用户名密码错误'})
        else:                                   # 如果表单数据不合法，返回login_form里的错误信息(未查询数据库)
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})      # 请求该页面时返回一个验证码图片

    def post(self, request):
        register_form = RegisterForm(request.POST)              # 表单和RegisterForm绑定
        if register_form.is_valid():
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')         # 取到的password是一个明文
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.password = make_password(password)     # 对明文密码进行加密
            user_profile.save()

            send_register_email(username, 'register')