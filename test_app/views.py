# -*- coding: utf-8 -*-

import hashlib
import json
import os
import requests
import rest_framework
import pymysql.cursors
import pymysql
import pandas as pds
import datetime
import jieba
import re

# from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django_redis import get_redis_connection
from django.core.files.base import ContentFile
from .models import User, Activity, Ticket
from .serializers import UserSerializer

appid = 'wx7d93bbb34a8d3662'
appsecret = '4acadab52b5a08cd3166d4743c39f3f8'

@api_view(['POST'])

# from code to session
def init(request):
    # code & userinfo
    js_code = request.POST.get('code')
    user_info = request.POST.get('info')

    # get openid
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + appsecret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)
    
    # if fail
    if 'errcode' in response:
        return Response(data={'code':response['errcode'], 'msg': response['errmsg']})

    # openid & session_key
    openid = response['openid']
    session_key = response['session_key']

    # save openid in database and make sure whether it is existing
    user, create = User.objects.get_or_create(openid=openid)

    # complete user info
    user.username = json.loads(user_info)['nickName']
    user.password = openid

    # save info
    user.save()

    # create jwt
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    jwt = jwt_encode_handler(payload)

    # ret msg
    ret = {'code': '000', 'msg': None,'data':{}}
    ret['msg'] = '授权成功'
    ret['data'] = {
        'jwt': jwt,
        'user_openid': user.openid,
        'nickname': user.username
    }
    return JsonResponse(ret)

# 现在getList会在返回活动列表的同时检测这些活动是否结束或者无票
def getActivityList(request):
    # 重写json序列化类，特判datetime类型（这个类不可写在函数外，否则将引起特殊问题）
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            # elif isinstance(obj, date):
            #     return obj.strftime("%Y-%m-%d")
            else:
                return json.JSONEncoder.default(self, obj)
    
    actList = Activity.objects.all()
    retList = []
    for item in actList:
        # update status
        current_time = datetime.datetime.now()
        if item.time <= current_time:
            item.status = u'已结束'
            item.heat = item.min_heat
        elif item.remain <= 0:
            item.status = u'已售空'
        item.save() # WARNING : 修改后必须save()一下，否则数据库中的数据不会发生变化
        i = {
            'activity_id': item.activity_id, 
            'title': item.title, 
            'image': 'http://62.234.50.47' + item.image.url,
            'status': item.status,
            'remain': item.remain,
            'publisher': item.publisher,
            'description': item.description,
            'time': item.time,
            'place': item.place, 
            'price': item.price,
            'heat': item.heat,
        }
        iJson = json.dumps(i, cls = DateEncoder) # 注意调用新的json序列化类
        retList.append(iJson)
    
    # ret msg
    ret = {'code': '001', 'msg': None,'data':{}}
    ret['msg'] = '获取活动列表成功'
    ret['data'] = {
        'activityList': retList,
    }
    return JsonResponse(ret)

def purchaseTicket(request):
    # code & userinfo
    js_code = request.POST.get('code')
    activity_id = request.POST.get('activity_id')

    # get openid
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + appsecret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)
    
    # if fail
    if 'errcode' in response:
        return Response(data={'code':response['errcode'], 'msg': response['errmsg']})

    # openid & session_key
    openid = response['openid']
    session_key = response['session_key']
    
    # get user & activity
    try: 
        user = User.objects.get(openid = openid)
        activity = Activity.objects.get(activity_id = activity_id)
    except:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '购票失败，用户或活动不存在'
        ret['data'] = {
            'code': js_code,
            'openid': openid,
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # is remain?
    if activity.remain <= 0:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '购票失败，余票不足'
        ret['data'] = {
            'user': user.username,
            'activity_id': activity_id,
            'remain': activity.remain,
        }
        return JsonResponse(ret)
    else:
        try:
            ticket = Ticket.objects.filter(owner = user)
            # print(ticket)
            for i in ticket:
                # print('owner:', i.owner.user_id, 'act:', i.activity.activity_id)
                if i.activity == activity:
                    ret = {'code': '102', 'msg': None,'data':{}}
                    ret['msg'] = '购票失败，票已存在'
                    ret['data'] = {
                        'user_id': user.user_id,
                        'user': user.username,
                        'activity_id': activity.activity_id,
                        'remain': activity.remain,
                    }
                    return JsonResponse(ret)
        except:
            pass

        # activity changes
        activity.remain -= 1 # decrease remain
        activity.heat += activity.purchase_change
        activity.save()

        # ticket changes
        ticket = Ticket(owner = user, activity = activity) # new ticket
        ticket.is_valid = True # varify
        ticket.save()
        
        # ret msg
        ret = {'code': '002', 'msg': None,'data':{}}
        ret['msg'] = '购票成功'
        ret['data'] = {
            'user_id': user.user_id,
            'user': user.username,
            'activity_id': activity.activity_id,
            'remain': activity.remain,
        }
        return JsonResponse(ret)

def getTicketList(request):
    # 引用新class
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return json.JSONEncoder.default(self, obj)

    # code & userinfo
    js_code = request.POST.get('code')

    # get openid
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + appsecret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)
    
    # if fail
    if 'errcode' in response:
        return Response(data={'code':response['errcode'], 'msg': response['errmsg']})

    # openid & session_key
    openid = response['openid']
    session_key = response['session_key']
    
    # get user
    try: 
        user = User.objects.get(openid = openid)
    except:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '获取已购票列表失败，用户不存在'
        ret['data'] = {
            'code': js_code,
            'openid': openid,
        }
        return JsonResponse(ret)

    # get user's tickets
    ticList = user.ticket_set.all()
    # print(ticList[0].activity.activity_id)

    # get retList
    retList = []
    for item in ticList:
        i = {
            'ticket_id': item.ticket_id,
            # 'owner': item.owner.username, 
            'ticket_status': item.is_valid,
            'activity_status': item.activity.status,
            'activity_image': 'http://62.234.50.47' + item.activity.image.url,
            # 'activity_id': item.activity.activity_id,
            'title': item.activity.title,
            'time': item.activity.time,
            'place': item.activity.place,
            'price': item.activity.price,
            'heat': item.activity.heat,
        }
        iJson = json.dumps(i, cls = DateEncoder)
        retList.append(iJson)

    # ret msg
    ret = {'code': '003', 'msg': None,'data':{}}
    ret['msg'] = '获取已购票列表成功'
    ret['data'] = {
        'user': user.username,
        'ticketList': retList,
    }
    return JsonResponse(ret)

def getActivityInfo(request):
    # code & userinfo
    activity_id = request.POST.get('activity_id')

    # get user & activity
    try: 
        activity = Activity.objects.get(activity_id = activity_id)
    except:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '获取活动详情失败，该活动不存在'
        ret['data'] = {
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # 浏览活动详情，改变活动热度
    activity.heat += activity.scan_change
    activity.save()

    # ret msg
    ret = {'code': '004', 'msg': None,'data':{}}
    ret['msg'] = '活动详情获取成功'
    ret['data'] = {
        'activity_id': activity_id,
        'title': activity.title,
        'image': 'http://62.234.50.47' + activity.image.url,
        'status': activity.status,
        'remain': activity.remain,
        'publisher': activity.publisher,
        'description': activity.description,
        'time': activity.time,
        'place': activity.place,
        'price': activity.price,
        'heat': activity.heat,
    }
    return JsonResponse(ret)

def getTicketInfo(request):
    # code & userinfo
    ticket_id = request.POST.get('ticket_id')

    # get user & activity
    try:
        ticket = Ticket.objects.get(ticket_id = ticket_id)
    except:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '获取票详情失败，票不存在'
        ret['data'] = {
            'ticket_id': ticket_id,
        }
        return JsonResponse(ret)

    # ret msg
    ret = {'code': '005', 'msg': None,'data':{}}
    ret['msg'] = '票详情获取成功'
    ret['data'] = {
        'ticket_id': ticket_id,
        'owner': ticket.owner.username,
        'title': ticket.activity.title,
        'price': ticket.activity.price,
        'place': ticket.activity.place,
        'heat': ticket.activity.heat,
        'tic_time': ticket.purchaseTime,
        'act_time': ticket.activity.time,
        'is_valid': ticket.is_valid,
        # 'QRCode': ticket.QRCode,
    }
    return JsonResponse(ret)

# 已修复，现在对于已经is_valid = False的票，不会重复退票
def refundTicket(request):
    # code & userinfo
    js_code = request.POST.get('code')
    ticket_id = request.POST.get('ticket_id')

    # get openid
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + appsecret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)
    
    # if fail
    if 'errcode' in response:
        return Response(data={'code':response['errcode'], 'msg': response['errmsg']})

    # openid & session_key
    openid = response['openid']
    session_key = response['session_key']
    
    # get user & activity
    try: 
        user = User.objects.get(openid = openid)
        ticket = Ticket.objects.get(ticket_id = ticket_id)
        activity = ticket.activity
    except: 
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '退票失败，用户或此票不存在'
        ret['data'] = {
            'code': js_code,
            'openid': openid,
            'ticket_id': ticket_id,
        }
        return JsonResponse(ret)

    # 判断ticket的is_valid，仅为True时才可退票
    if ticket.is_valid:
        # activity changes
        activity.remain += 1
        activity.heat -= activity.purchase_change
        activity.save()

        # ticket changes
        ticket.is_valid = False # unvarify
        ticket.save()

        # user changes ?

        # ret msg
        ret = {'code': '006', 'msg': None,'data':{}}
        ret['msg'] = '退票成功'
        ret['data'] = {
            'ticket_id': ticket_id,
            'unvarify': ticket.is_valid,
        }
    else:
        # ret msg
        ret = {'code': '006', 'msg': None,'data':{}}
        ret['msg'] = '退票失败'
        ret['data'] = {
            'ticket_id': ticket_id,
            'unvarify': ticket.is_valid,
        }
    return JsonResponse(ret)

def searchEngine(request):
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            # elif isinstance(obj, date):
            #     return obj.strftime("%Y-%m-%d")
            else:
                return json.JSONEncoder.default(self, obj)

    line = request.POST.get('line')

    wordList = jieba.lcut_for_search(line)
    actList = Activity.objects.all()
    retList = {}

    for item in actList:
        # update status
        current_time = datetime.datetime.now()
        if item.time <= current_time:
            item.status = u'已结束'
            item.heat = item.min_heat
        elif item.remain <= 0:
            item.status = u'已售空'
        item.save() 

    # search
    for word in wordList:
        for act in actList:
            size = len(re.findall(word, act.title)) + \
                len(re.findall(word, act.publisher)) + \
                len(re.findall(word, act.description)) + \
                len(re.findall(word, act.place))
            if size > 0:
                if act.activity_id not in retList:  
                    retList[act.activity_id] = {}
                retList[act.activity_id][word] = size

    # sort with len
    sortedList = sorted(retList.items(), key = lambda x:len(x[1]), reverse=True)
    
    # trans list into dic
    retactList = []
    for item in sortedList:
        item = Activity.objects.get(activity_id=item[0])
        i = {
                'activity_id': item.activity_id, 
                'title': item.title, 
                'image': 'http://62.234.50.47' + item.image.url,
                'status': item.status,
                'remain': item.remain,
                'publisher': item.publisher,
                'description': item.description,
                'time': item.time,
                'place': item.place, 
                'price': item.price,
                'heat': item.heat,
            }
        iJson = json.dumps(i, cls = DateEncoder) # 注意调用新的json序列化类
        retactList.append(iJson)

    # ret
    ret = {'code': '007', 'msg': None,'data':{}}
    ret['msg'] = '搜索成功'
    ret['data'] = {
        'actList': retactList,
    }
    return JsonResponse(ret)

def starActivity(request):
    # code & userinfo
    js_code = request.POST.get('code')
    activity_id = request.POST.get('activity_id')

    # get openid
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + appsecret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)
    
    # if fail
    if 'errcode' in response:
        return Response(data={'code':response['errcode'], 'msg': response['errmsg']})

    # openid & session_key
    openid = response['openid']
    session_key = response['session_key']
    
    # get user & activity
    try: 
        user = User.objects.get(openid = openid)
        activity = Activity.objects.get(activity_id = activity_id)
    except:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '收藏失败，用户或活动不存在'
        ret['data'] = {
            'code': js_code,
            'openid': openid,
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # star
    user.starred.add(activity)
    activity.heat += activity.star_change
    
    # save
    user.save()
    activity.save()

    # ret msg
    ret = {'code': '008', 'msg': None,'data':{}}
    ret['msg'] = '收藏成功'
    ret['data'] = {
        'user': user.username,
        'activity': activity.activity_id,
    }
    return JsonResponse(ret)

def getStarList(request):
    # code & userinfo
    js_code = request.POST.get('code')
    
    # get openid
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + appsecret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)
    
    # if fail
    if 'errcode' in response:
        return Response(data={'code':response['errcode'], 'msg': response['errmsg']})

    # openid & session_key
    openid = response['openid']
    session_key = response['session_key']
    
    # get user & activity
    try: 
        user = User.objects.get(openid = openid)
    except:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '获取收藏列表失败，该用户不存在'
        ret['data'] = {
            'code': js_code,
            'openid': openid,
        }
        return JsonResponse(ret)

    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            # elif isinstance(obj, date):
            #     return obj.strftime("%Y-%m-%d")
            else:
                return json.JSONEncoder.default(self, obj)
    
    actList = user.starred.all()
    retList = []
    for item in actList:
        # update status
        current_time = datetime.datetime.now()
        if item.time <= current_time:
            item.status = u'已结束'
            item.heat = item.min_heat
        elif item.remain <= 0:
            item.status = u'已售空'
        item.save() # WARNING : 修改后必须save()一下，否则数据库中的数据不会发生变化
        i = {
            'activity_id': item.activity_id, 
            'title': item.title, 
            'image': 'http://62.234.50.47' + item.image.url,
            'status': item.status,
            'remain': item.remain,
            'publisher': item.publisher,
            'description': item.description,
            'time': item.time,
            'place': item.place, 
            'price': item.price
        }
        iJson = json.dumps(i, cls = DateEncoder) # 注意调用新的json序列化类
        retList.append(iJson)
    
    # ret msg
    ret = {'code': '009', 'msg': None,'data':{}}
    ret['msg'] = '收藏列表获取成功'
    ret['data'] = {
        'activityList': retList,
    }
    return JsonResponse(ret)

def deleteStar(request):
    # code & userinfo
    js_code = request.POST.get('code')
    activity_id = request.POST.get('activity_id')

    # get openid
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + appsecret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)
    
    # if fail
    if 'errcode' in response:
        return Response(data={'code':response['errcode'], 'msg': response['errmsg']})

    # openid & session_key
    openid = response['openid']
    session_key = response['session_key']
    
    # get user & activity
    try: 
        user = User.objects.get(openid = openid)
        activity = Activity.objects.get(activity_id = activity_id)
    except: 
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '取消收藏失败，该用户或活动不存在'
        ret['data'] = {
            'code': js_code,
            'openid': openid,
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # delete
    user.starred.remove(activity)
    activity.heat -= activity.star_change

    # save
    user.save()
    activity.save()

    # ret msg
    ret = {'code': '010', 'msg': None,'data':{}}
    ret['msg'] = '取消收藏成功'
    ret['data'] = {
        'user': user.username,
        'activity': activity.activity_id,
    }
    return JsonResponse(ret)

# 初始化测试数据库
def saveTestData(request):
    # test data for user
    openid = 'testOpenid'

    user, created = User.objects.get_or_create(openid = openid)
    user_str = str(UserSerializer(user).data)

    user.username = 'testUser'
    user.password = openid

    user.save()

    # test data for acvivity
    activity1, created = Activity.objects.get_or_create(title = 'testActivity 1')

    activity1.remain = 100
    activity1.time = '2019-12-30 12:30:00'
    activity1.place = '大礼堂'
    activity1.price = 123
    activity1.publisher = '软件学院项目部'
    # activity1.heat = 10.0

    activity1.save()

    activity2, created = Activity.objects.get_or_create(title = 'testActivity 5')
    activity2.remain = 50
    activity2.time = '2019-12-01 12:30:00'
    activity2.place = '紫荆操场'
    activity2.price = 50
    activity2.description = '这是一场足球比赛。'
    activity2.publisher = '清华大学足球协会'
    # activity2.heat = 9.9

    activity2.save()

    # # test data for ticket
    # ticket = Ticket(owner = user, activity = activity)
    # ticket.save()
    
    # ret msg
    ret = {'code': '011', 'msg': None,'data':{}}
    ret['msg'] = '保存成功'
    ret['data'] = {
        'newUser': user.username,
        'newActivity': [activity1.title, activity2.title]
        # 'newTicket': ticket.ticket_id,
    }
    return JsonResponse(ret)

def index(request):
    return HttpResponse("Hello! You are at the index page of test_app.")
