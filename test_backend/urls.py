"""test_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from test_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # admin
    path('admin/', admin.site.urls), # 管理

    # test
    path('index/', views.index), # HelloWorld测试界面

    # init
    path('init/', views.init), #授权

    # activity
    path('getActivityList/', views.getActivityList), # 获取活动列表
    path('getActivityInfo/', views.getActivityInfo), # 获取活动详情 
    path('getScrollActivity/', views.getScrollActivity), # 获取滚图活动
    path('searchEngine/', views.searchEngine), # 搜索 

    # ticket
    path('purchaseTicket/', views.purchaseTicket), # 购票 
    path('refundTicket/', views.refundTicket), # 退票 
    path('getTicketList/', views.getTicketList), # 获取已购票列表 
    path('getTicketInfo/', views.getTicketInfo), # 获取票的详情 

    # star
    path('starActivity/', views.starActivity), # 收藏
    path('deleteStar/', views.deleteStar), # 取消收藏
    path('getStarList/', views.getStarList), # 获取收藏列表

    # save test data
    path('saveTestData/', views.saveTestData), # 存入测试数据 

    # QRCode
    path('testQRCode/', views.testQRCode),
    path('logo/', views.logo),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
