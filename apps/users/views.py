# coding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from users.models import UserProfile, EmailVerifyRecord
from users.forms import LoginForm, RegisterForm, ForgetForm, ResetPasswordForm
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
                if user.is_active:
                    login(request, user)                        # 根据用户信息生成一个session
                    return render(request, 'index.html')    # 登陆成功，返回首页
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:                                           # (查询数据库之后)用户名密码出错返回错误msg
                return render(request, 'login.html', {'msg': '用户名密码错误'})
        else:                                   # 如果表单数据不合法，返回login_form里的错误信息(未查询数据库)
            return render(request, 'login.html', {'login_form': login_form})


class ActiveUserView(View):
    def get(self, request, active_code):    # 用户点击验证链接，进入到此方法进行处理，active_code是随机字符串
        all_records = EmailVerifyRecord.objects.filter(code=active_code)    # 根据验证码在数据库中查询满足条件的记录
        if all_records:
            for record in all_records:
                email = record.email                            # 取出满足条件的记录的email地址
                user = UserProfile.objects.get(email=email)     # 用email找到UserProfile表中的user用户
                user.is_active = True                           # 把用户激活状态设为True
                user.save()                                     # 保存到数据库
        else:
            return render(request, 'active_fail.html')          # 返回链接失效页面
        return render(request, 'login.html')                    # 点击验证连接后，激活成功，跳到登录界面


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})      # 请求该页面时返回一个验证码图片

    def post(self, request):
        register_form = RegisterForm(request.POST)              # 表单和RegisterForm绑定
        if register_form.is_valid():                    # 判断输入是否合法
            username = request.POST.get('email', '')
            if UserProfile.objects.filter(email=username):  # 判断邮箱有没有被注册过
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            password = request.POST.get('password', '')         # 取到的password是一个明文
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False
            user_profile.password = make_password(password)     # 对明文密码进行加密
            user_profile.save()                                 # 存储到数据库中

            send_register_email(username, 'register')           # 给用户发送验证邮件
            return render(request, 'login.html')                # 注册成功返回登录页面
        else:
            return render(request, 'register.html', {'register_form': register_form})   # 注册失败返回错误信息


class ForgetPasswordView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})      # 验证码图片返回前台

    def post(self, request):
        forget_form = ForgetForm(request.POST)          # post方法要传request.POST
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')        # 用于找回密码的邮箱验证
            return render(request, 'send_success.html') # 提示邮件发送成功
        else:                                           # 否则还是返回找回密码页面
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPasswordHtmlView(View):
    def get(self, request, active_code):    # 用户点击验证链接，进入到此方法进行处理，active_code是随机字符串
        all_records = EmailVerifyRecord.objects.filter(code=active_code)    # 根据验证码在数据库中查询满足条件的记录
        if all_records:
            for record in all_records:
                email = record.email                            # 取出满足条件的记录的email地址
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')          # 返回链接失效页面
        return render(request, 'login.html')


class ResetPasswordView(View):
    def post(self, request):
        reset_form = ResetPasswordForm(request.POST)
        if reset_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if password1 != password2:
                return render(request, 'password_reset.html', {'msg': '两次密码输入不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password1)    # 明文密码加密
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'reset_form': reset_form})