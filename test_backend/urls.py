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
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('init/', views.init),
    path('getActivityList/', views.getActivityList),
    path('purchaseTicket/', views.purchaseTicket),
    path('getTicketList/', views.getTicketList),
    path('getActivityInfo/', views.getActivityInfo),
    path('getTicketInfo/', views.getTicketInfo),
    path('refundTicket/', views.refundTicket),
    path('searchEngine/', views.searchEngine),
    path('saveTestData/', views.saveTestData),
    path('changeData/', views.changeData),
    # path('showPicture/', views.showPicture),
    # path('getPath/', views.getPath),
    # TODO 搜索功能
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 