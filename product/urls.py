from django.urls import path
from product import views

app_name = '[product]'  # 这里的命名需和文件夹名字一样
urlpatterns = [
    path("", views.index, name="index"),
]
