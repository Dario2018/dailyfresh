from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from user.models import UserAddress
from django_redis import get_redis_connection
from product.models import ProductSKU


# Create your views here.

class LoginRequiredMixin(object):
    """这个是必须要先登录之后才能访问"""

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        address = UserAddress.objects.get_default_addr(user)

        # from redis import StrictRedis
        # sr = StrictRedis(host="192.168.187.128", port=6379, db=5)

        con = get_redis_connection("default")  # 和setting字段对应
        history_key = "history_%d" % user.id
        # 前五条数据
        history_ids = con.lrange(history_key, 0, 4)
        products_list = []
        for p_id in history_ids:
            product = ProductSKU.objects.get(id=p_id)
            products_list.append(product)

        return render(request, "user_center_info.html", {"address": address, "product_list": products_list})


class UserAddressView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        address = UserAddress.objects.get_default_addr(user)
        return render(request, "user_address.html", {"address": address})

    def post(self, request):
        user = request.user
        recipient = request.POST["recipient"]
        address = request.POST["address"]
        try:
            zip_code = int(request.POST['zip_code'])
        except Exception:
            pass
        phone = request.POST["phone"]
        default_addr = UserAddress.objects.get_default_addr(user)
        if default_addr:
            is_default = False
        else:
            is_default = True
        UserAddress.objects.create(recipient=recipient, address=address, zip_code=zip_code, contact_num=phone,
                                   is_default=is_default, user=user)
        return redirect(request, 'user:useraddress')
