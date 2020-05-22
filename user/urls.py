"""拷贝过来的
"""
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = '[user]'
urlpatterns = [
    path("userinfo", login_required(views.UserInfoView.as_view()), name="userinfo"),
    path("useraddress", login_required(views.UserAddressView.as_view()), name="useraddress")
]
