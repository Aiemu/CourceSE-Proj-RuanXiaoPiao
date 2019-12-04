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
    path('admin/', admin.site.urls), # 管理
    path('index/', views.index), # HelloWorld测试界面
    path('init/', views.init), #授权
    path('getActivityList/', views.getActivityList), # 获取活动列表
    path('purchaseTicket/', views.purchaseTicket), # 购票
    path('getTicketList/', views.getTicketList), # 获取已购票列表
    path('getActivityInfo/', views.getActivityInfo), # 获取活动详情
    path('getTicketInfo/', views.getTicketInfo), # 获取票的详情
    path('refundTicket/', views.refundTicket), # 退票
    path('searchEngine/', views.searchEngine), # 搜索
    path('saveTestData/', views.saveTestData), # 存入测试数据
    path('starActivity/', views.starActivity), # 收藏
    path('deleteStar/', views.deleteStar), # 取消收藏
    path('getStarList/', views.getStarList), # 获取收藏列表


    # path('testImage/', views.testImage),
    # path('globalTest/',views.globalTest), # 全局变量测试
    # path('changeData/', views.changeData), # 
    # path('showPicture/', views.showPicture),
    # path('getPath/', views.getPath),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
