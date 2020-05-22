from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from product.models import TypeShow


# Create your views here.

@login_required
def index(request):
    result = {}
    result["typeShowlist"] = TypeShow.objects.all()
    for key in result:
        print(result[key])
    return render(request, "index.html", result)
