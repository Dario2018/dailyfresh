"""拷贝过来的
"""
from django.urls import path, re_path
from django.conf.urls import url
from login.views import LoginView, ActiveView, RegisterView, ErrorView, LogoutView, ForgotPassWord, test

app_name = '[login]'
urlpatterns = [
    path("", LoginView.as_view()),
    path("register", RegisterView.as_view(), name="register"),
    path("register.html", RegisterView.as_view()),
    re_path("active/(?P<token>.*)", ActiveView.as_view(), name="active"),
    path("", LoginView.as_view(), name="login"),
    path("error.html", ErrorView.as_view(), name="error"),
    path("loginout", LogoutView.as_view(), name="logout"),
    path("test", test),
    url(r"^logout$", LoginView.as_view(), name="logout"),
    path("forgotPassword", ForgotPassWord.as_view(), name="forgotPassword")
]
