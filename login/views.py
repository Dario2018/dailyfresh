from django.shortcuts import render, redirect, reverse
from user.models import User
from django.views.generic import View
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from celery_tasks.tasks import send_register_active_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import re
import logging


# Create your views here.


def test(request):
    return render(request, "test.html")


# def login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         pwd = request.POST.get("pwd")
#         user = User.objects.get(username=username)
#         if user is None or user.password != pwd:
#             return render(request, "index.html", {"magess": "用户名或密码不正确"})
#         return render(request, "index.html")
#     elif request.method == "GET":
#         return render(request, "login.html")
#     else:
#         return render(request, "404.html")

class LoginView(View):
    """登录"""

    def post(self, request):
        username = request.POST.get("username")
        pwd = request.POST.get("pwd")
        print("username=", username, "pwd=", pwd)
        if not all([username, pwd]):
            return render(request, "login.html", {"message": "用户名和密码都不能为空"})
        user = authenticate(username=username, password=pwd)
        if user is not None:
            if user.is_active:
                # 用户已经激活，记录用户的登录状态
                login(request, user)
                # 跳转到首页
                response = redirect((reverse("product:index")))
                # 判断是否需要记住用户名
                remember = request.POST.get("remember")
                print("remember=", remember)
                if remember == "on":
                    response.set_cookie("username", username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie("username")
                # 返回response
                return response
            else:
                return render(request, "login.html", {"message": "用户未激活。"})
        else:
            return render(request, "login.html", {"message": "用户名或密码不正确。"})

    def get(self, request):
        print("进入登录页面。。。")
        # 判断是否记住了用户名
        if "username" in request.COOKIES:
            username = request.COOKIES.get("username")
            checked = "checked"
        else:
            username = ""
            checked = ""
        return render(request, "login.html", {"username": username, "checked": checked})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, "login.html")


# def register(request):
#     if request.method == "POST":
#         body = request.POST
#         username = body.get("user_name")
#         pwd = body.get("pwd")
#         cpwd = body.get("cpwd")
#         email = body.get("email")
#         allow = body.get("allow")
#         if not all([username, pwd, cpwd, email, allow]):
#             return render(request, "register.html", {"status": -200, "massage": "数据不完整"})
#         # 校验邮箱
#         if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
#             return render(request, "register.html", {"status": -200, "massage": "邮箱格式不正确"})
#         if pwd != cpwd:
#             return render(request, "register.html", {"status": -200, "message": "密码不一致"})
#         if allow is None:
#             return render(request, "register.html", {"status": -200, "massage": "请同意协议！"})
#         # user = User()
#         # user.username = username
#         # user.password = pwd
#         # user.email = email
#         # user.is_active = True
#         # user.save()
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             user = None
#         if user:
#             return render(request, "register.html", {"status": -200, "massage": "该用户已存在"})
#         user = User.objects.create_user(username, email, pwd)
#         user.is_active = 0
#         user.save()
#
#         # 加密用户的身份证，生成token
#         serializer = Serializer(settings.SECRET_KEY, 3600)
#         info = {"confirm": user.id}
#         token = serializer.dumps(info)  # byte
#         token = token.decode()
#         # 同步发邮件1-
#         # subject = "天天生鲜欢迎信息"
#         # message = ""
#         # sender = settings.EMAIL_FROM
#         # receivers = [email]
#         # html_message = "<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的的账号<br/><a href='http://127.0.0.1:8000/login/active/%s'>http://127.0.0.1:8000/login/active/%s</a>" % (
#         #     username, token, token)
#         # # 这里此方法是同步发送的，可能由于网络IO 引起 阻塞卡顿
#         # send_mail(subject, message, sender, receivers, html_message=html_message)
#         # 异步发邮件-2
#         send_register_active_email.delay(email, username, token)
#         return redirect(reverse("product:index"))
#     elif request.method == "GET":
#         print("register get...")
#         return render(request, "register.html")
#     else:
#         return render(request, "404.html")

class ForgotPassWord(View):
    """忘记密码"""

    def get(self, request):
        print("hello forgot html...")
        return render(request, "forgotPassword.html")

    def post(self, requeste):
        pass


class RegisterView(View):
    # 类视图使用
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        body = request.POST
        username = body.get("user_name")
        pwd = body.get("pwd")
        cpwd = body.get("cpwd")
        email = body.get("email")
        allow = body.get("allow")
        if not all([username, pwd, cpwd, email, allow]):
            return render(request, "register.html", {"status": -200, "massage": "数据不完整"})
        # 校验邮箱
        if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return render(request, "register.html", {"status": -200, "massage": "邮箱格式不正确"})
        if pwd != cpwd:
            return render(request, "register.html", {"status": -200, "message": "密码不一致"})
        if allow is None:
            return render(request, "register.html", {"status": -200, "massage": "请同意协议！"})
        # user = User()
        # user.username = username
        # user.password = pwd
        # user.email = email
        # user.is_active = True
        # user.save()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, "register.html", {"status": -200, "massage": "该用户已存在"})
        user = User.objects.create_user(username, email, pwd)
        user.is_active = 0
        user.save()

        # 加密用户的身份证，生成token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {"confirm": user.id}
        token = serializer.dumps(info)  # byte
        token = token.decode()
        # 同步发邮件1-
        # subject = "天天生鲜欢迎信息"
        # message = ""
        # sender = settings.EMAIL_FROM
        # receivers = [email]
        # html_message = "<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的的账号<br/><a href='http://127.0.0.1:8000/login/active/%s'>http://127.0.0.1:8000/login/active/%s</a>" % (
        #     username, token, token)
        # # 这里此方法是同步发送的，可能由于网络IO 引起 阻塞卡顿
        # send_mail(subject, message, sender, receivers, html_message=html_message)
        # 异步发邮件-2
        send_register_active_email.delay(email, username, token)
        return redirect(reverse("product:index"))


class ActiveView(View):
    """用户激活"""

    def get(self, request, token):
        """用户激活"""
        print("token=", token)
        # 解密
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活的用户id
            user_id = info["confirm"]
            print("user_id==", user_id)
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转到登录页面
            return redirect(reverse("login:login"))
        except SignatureExpired as e:
            # 激活链接已经过期
            return HttpResponse("激活链接已经过期")


class ErrorView(View):
    def get(self, request):
        return render(request, "404.html")
