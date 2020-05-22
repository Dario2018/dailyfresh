"""拷贝过来的
"""
from django.urls import path
from order.views import UserCenterOrderView

app_name = '[order]'
urlpatterns = [
    path("userOrderCenter", UserCenterOrderView.as_view(), name="usercenterorder")
]
