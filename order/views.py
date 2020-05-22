from django.shortcuts import render
from django.views.generic import View
from user.views import LoginRequiredMixin


# Create your views here.
def order(request):
    return render(request, "user_center_order.html")


class UserCenterOrderView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "user_center_order.html")

    def post(self, request):
        pass
