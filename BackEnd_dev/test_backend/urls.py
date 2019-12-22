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

'''
状态码为三位，形如：000
首位为状态描述，0为成功，1为用户异常，2为活动异常，3为票异常，4为其他异常
后两位标记函数
    第二位为Part序号标记
    末位为Part中的函数序号
'''

urlpatterns = [
    # Part 0: init
    path('init/', views.init), # 授权 00
    path('verifyUser/', views.verifyUser), # 认证 01

    # Part 1: activity
    path('getActivityList/', views.getActivityList), # 获取活动列表 10
    path('getActivityInfo/', views.getActivityInfo), # 获取活动详情 11
    path('getScrollActivity/', views.getScrollActivity), # 获取滚图活动 12
    path('searchEngine/', views.searchEngine), # 搜索 13
    path('getTimeSortedActivity/', views.getTimeSortedActivity), # 按时间排序 14
    path('getHeatSortedActivity/', views.getHeatSortedActivity), # 按热度排序 15
    path('addActivity/', views.addActivity), # 添加活动 16

    # Part 2: ticket
    path('purchaseTicket/', views.purchaseTicket), # 购票 20
    path('refundTicket/', views.refundTicket), # 退票 21
    path('getTicketList/', views.getTicketList), # 获取已购票列表 22
    path('getTicketInfo/', views.getTicketInfo), # 获取票的详情 23
    path('checkTicket/', views.checkTicket), # 检票端检票 24

    # Part 3: star
    path('starActivity/', views.starActivity), # 收藏 30
    path('deleteStar/', views.deleteStar), # 取消收藏 31
    path('getStarList/', views.getStarList), # 获取收藏列表 32

    # Part 4: save test data
    path('saveTestData/', views.saveTestData), # 存入测试数据 40

    # Part 5: test
    path('index/', views.index), # 测试界面 50

    # Part 6: admin
    path('admin/', admin.site.urls), # 管理 60

    path('random/', views.randomStr),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
