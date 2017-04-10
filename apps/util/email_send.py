# coding: utf-8
__author__ = 'gocjy'
__date__ = '2017/4/1 17:02'

from django.core.mail import send_mail

import random

from users.models import EmailVerifyRecord
from OMooc.settings import EMAIL_FROM


# 生成一个随机字符串(激活码)
def generate_random_code(randomlength=8):
    random_code = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkMmNnLlOoPpQqRrSsTtUuVvWwXxYyZz0123456789#?'
    length = len(chars) - 1
    for i in range(randomlength):
        random_code += chars[random.randint(0 ,length)]
    return random_code


# 发送注册邮件
def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    random_code = generate_random_code(16)
    email_record.email = email
    email_record.code = random_code
    email_record.send_type = send_type
    email_record.save()
    # 发送邮件↓
    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'OMooc注册帐号激活连接'
        email_body = '请点击下面的链接激活帐号：http://127.0.0.1:8000/active/{0}'.format(random_code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        print '注册邮件已发送'
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = 'OMooc帐号密码重置'
        email_body = '请点击下面的链接重置密码：http://127.0.0.1:8000/reset/{0}'.format(random_code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        print '重置密码邮件已发送'
        if send_status:
            pass