#有关python开发项目过程中笔录#
1.连接MySQL需要修改虚拟环境下文件，分别是django/db/backends/base.py 和 operations.py
2.创建要给超级用户，用户名：dario  邮箱：dario@dario.cn 密码：chen2018
  创建要给超级用户，用户名：chen  邮箱：dario@dario.cn 密码：chen2018
  启动项目：python manage.py runserver 127.0.0.1:8000  登录后台：127.0.0.1:8000/admin
3.创建一个项目命令：python startproject test1
4.创建一个应用命令：python startapp booktest1
5.创建模型类的过程命令：python manage.py 
#遇到的问题
1.OSError: [WinError 123] 文件名、目录名或卷标语法不正确。: '<frozen importlib._bootstrap>'
##开发register 模块过程：
（1）新建一个应用，命令为：python manage.py startapp login
 (2) 创建模型类：再models.py 文件创建，继承基础类型，每个class有一个元类Meta，在把模型类相关映射到数据库需要使用以下两条命令：
    python manage.py makemigrations
    python manage.py migrate
 (3) 需要注意时间的默认值由于版本不同而产生不同的复制，注意choice的使用
（4）对于要进入页面需要再页面中的form标签中写上csrf_token-跨站点请求伪造
（5）注意all()方法的使用
（6）在该模块中最重要的时要是要懂redirect(reverse("produc:index")),期间需要注意namespace 和在该应用的urls.py 下 的urlpatter前些app_name="[应用名]"，具体要参考register的登录过程
（7）学习心得：对与学习要举一反三，做到灵活应用。
 (8)select * from userinfo \G; 可以竖着显示
 (9) 加密 pip install itsdangerous
 2.注册模块
 （1）使用seler异步发送信息
 （2）启动celery worker端 进入到项目根目录下，输入命令:celery -A celery_tasks.tasks worker -l info ，目前这个是任务发送，而
        D:\workplaces\WebstormProjects\dailyfresh 是worker.
 （3）pip install django-redis 来安装支持缓存
 （4）Mixin 的使用：需要用户登录才能访问，比如LoginRequiredMixin,没有登录，则根据setting 配置的LOGIN_URL 进行跳转，并且后面带上text="你原先访问的地址"
 （5）request.user.is_authenticated()拦截每一个请求，如果用户已登录，则返回为True
 （6）模型管理器类方法封装，代码的抽取相同部分进行封装
 （7）使用redis保存用户的浏览记录，分两种情况：第一是如设计的存储时所有用户的 浏览记录用一条数据保存，则使用redis 的hash history: userr_用户id:1234,
        如果时每个用户的历史浏览记录用一条数据保存：则使用list history_用户id:[3,4,5]
 （8）http://192.168.187.128/group1/M00/00/00/wKi7gF2lvjuACAU5AAAADBSRxKc073.txt 可以访问a.txt内容
 （9）fdfs修改文件之后pip install mutagen 和pip install requests
