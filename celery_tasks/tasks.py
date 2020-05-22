# 使用celery 异步发邮件
from django.shortcuts import render
from django.core.mail import send_mail
from django.template import loader, RequestContext
from django.conf import settings
from celery import Celery
import time
import os
import django

# # 在任务处理一端加这句，任务发送者不需要加
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
# django.setup()

# 需要放到setup下面
from product.models import ProductCategory, ProductBanner, PromotionPc, TypeShow

celery_app = Celery('celery_tasks.tasks', broker="redis://192.168.187.128:6379/8")


# 定义任务函数
@celery_app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    subject = "天天生鲜欢迎信息"
    message = ""
    sender = settings.EMAIL_FROM
    receivers = [to_email]
    html_message = "<h1>%s,欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的的账号<br/><a href='http://127.0.0.1:8000/login/active/%s'>http://127.0.0.1:8000/login/active/%s</a>" % (
        username, token, token)
    # 这里此方法是同步发送的，可能由于网络IO 引起 阻塞卡顿
    send_mail(subject, message, sender, receivers, html_message=html_message)
    time.sleep(5)


@celery_app.task
def generate_static_index_html(request):
    """产生首页静态页面"""

    types = ProductCategory.objects.all()
    # 获取首页轮播商品信息
    goods_banners = ProductBanner.objects.all().order_by("index")
    # 获取首页促销活动信息
    promotion_banners = PromotionPc.objects.all().order_by("index")
    # 获取首页分类商品展示信息
    for type in types:
        image_banners = TypeShow.objects.filter(type=type, display_type=1).order_by("index")
        title_banners = TypeShow.objects.filter(type=type, display_type=0).order_by("index")
        type.image = image_banners
        type.logo = title_banners
    # 组织模板上下文
    context = {"types": types, "goods_banners": goods_banners, "promotion_banners": promotion_banners}
    # 1.加载模板文件
    temp = loader.get_template("template_static_index_html.html")
    # context=RequestContext(request,context)
    static_index_html = temp.render(context)
    # 生成首页对应的静态文件
    save_path = os.path.join(settings.BASE_DIR, "static/indexTemp.html")
    with open(save_path, "w") as f:
        f.write(static_index_html)
