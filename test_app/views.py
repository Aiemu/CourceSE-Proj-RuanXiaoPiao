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
import qrcode

# from django.conf import settings
from PIL import Image
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



'''
Part 0
Intro: Function to init
Num: 1
List: 
    - init(request)
'''

@api_view(['POST'])

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
        'openid': user.openid,
        'nickname': user.username
    }
    return JsonResponse(ret)



'''
Part 1
Intro: Functions to operate activity
Num: 4
List: 
    - getActivityList(request)
    - getScrollActivity(request)
    - getActivityInfo(request)
    - searchEngine(request)
'''

def getActivityList(request):
    # encode date
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return json.JSONEncoder.default(self, obj)
    
    # get list
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
        
        # save
        item.save() 

        # create json
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

def getActivityInfo(request):
    # get activity_id
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

def getScrollActivity(request):
    # 重写json序列化类，特判datetime类型（这个类不可写在函数外，否则将引起特殊问题）
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            # elif isinstance(obj, date):
            #     return obj.strftime("%Y-%m-%d")
            else:
                return json.JSONEncoder.default(self, obj)
    
    actList = Activity.objects.filter(status = '正在抢票').order_by('-heat')
    retList = []
    count = 0
    for item in actList:
        # update status
        current_time = datetime.datetime.now()
        if item.time <= current_time:
            item.status = u'已结束'
            item.heat = item.min_heat
        elif item.remain <= 0:
            item.status = u'已售空'
        item.save() # WARNING : 修改后必须save()一下，否则数据库中的数据不会发生变化
        if count < 5:
            i = {
                'activity_id': item.activity_id, 
                'image': 'http://62.234.50.47' + item.image.url,
                'heat': item.heat,
            }
            iJson = json.dumps(i, cls = DateEncoder) # 注意调用新的json序列化类
            retList.append(iJson)
            count += 1
        else:
            break
    
    # ret msg
    ret = {'code': '001', 'msg': None,'data':{}}
    ret['msg'] = '获取活动列表成功'
    ret['data'] = {
        'activityList': retList,
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



'''
Part 2
Intro: Functions to operate ticket
Num: 4
List: 
    - purchaseTicket(request)
    - refundTicket(request)
    - getTicketList(request)
    - getTicketInfo(request)
'''

def purchaseTicket(request):
    # get openid & activity_id
    openid = request.POST.get('openid')
    activity_id = request.POST.get('activity_id')
    
    # get user & activity
    try: 
        user = User.objects.get(openid = openid)
    except:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '购票失败，该用户不存在'
        ret['data'] = {
            'openid': openid,
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # get activity
    try: 
        activity = Activity.objects.get(activity_id = activity_id)
    except:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '购票失败，该活动不存在'
        ret['data'] = {
            'openid': openid,
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # check remain
    if activity.remain <= 0:
        # ret msg
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
            # get user's ticket
            ticket = Ticket.objects.filter(owner = user)

            for i in ticket:
                # check is_valid
                if i.activity == activity and i.is_valid:
                    #ret msg
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

        # update activity's remain, heat
        activity.remain -= 1
        activity.heat += activity.purchase_change

        # save activity
        activity.save()

        # create new ticket
        ticket = Ticket(owner = user, activity = activity)
        
        # varify ticket
        ticket.is_valid = True 

        # save ticket
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

def refundTicket(request):
    # get ticket_id
    ticket_id = request.POST.get('ticket_id')

    # get activity
    try: 
        ticket = Ticket.objects.get(ticket_id = ticket_id)
        activity = ticket.activity
    except: 
        # ret msg
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '退票失败，该票不存在'
        ret['data'] = {
            'openid': openid,
            'ticket_id': ticket_id,
        }
        return JsonResponse(ret)

    # check is_valid
    if ticket.is_valid:
        # update activity's remain & heat
        activity.remain += 1
        activity.heat -= activity.purchase_change

        # save
        activity.save()

        # update ticket's is_valid
        ticket.is_valid = False

        # save
        ticket.save()

        # ret msg
        ret = {'code': '006', 'msg': None,'data':{}}
        ret['msg'] = '退票成功'
        ret['data'] = {
            'ticket_id': ticket_id,
            'is_valid': ticket.is_valid,
        }

    else:
        # ret msg
        ret = {'code': '006', 'msg': None,'data':{}}
        ret['msg'] = '退票失败，该票已为退票状态'
        ret['data'] = {
            'ticket_id': ticket_id,
            'is_valid': ticket.is_valid,
        }
    return JsonResponse(ret)

def getTicketList(request):
    # encode date
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return json.JSONEncoder.default(self, obj)

    # get openid
    openid = request.POST.get('openid')

    # get user
    try: 
        user = User.objects.get(openid = openid)
    except:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '获取已购票列表失败，用户不存在'
        ret['data'] = {
            # 'code': js_code,
            'openid': openid,
        }
        return JsonResponse(ret)

    # get user's tickets
    ticList = user.ticket_set.all()

    # get retList
    retList = []
    for item in ticList:
        # create json
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
        'openid': openid,
        'ticketList': retList,
    }
    return JsonResponse(ret)

def getTicketInfo(request):
    # get ticket_id
    ticket_id = request.POST.get('ticket_id')

    # get ticket
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



'''
Part 3
Intro: Functions to operate star
Num: 3
List: 
    - starActivity(request)
    - deleteStar(request)
    - deleteStar(request)
'''

def starActivity(request):
    # get openid & activity_id
    openid = request.POST.get('openid')
    activity_id = request.POST.get('activity_id')
    
    # get user
    try: 
        user = User.objects.get(openid = openid)

    except:
        # ret msg
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '收藏失败，该用户不存在'
        ret['data'] = {
            'openid': openid,
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # get activity
    try: 
        activity = Activity.objects.get(activity_id = activity_id)

    except:
        # ret msg
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '收藏失败，该活动不存在'
        ret['data'] = {
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
    # get openid
    openid = request.POST.get('openid')
    
    # get user
    try: 
        user = User.objects.get(openid = openid)
    except:
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '获取收藏列表失败，该用户不存在'
        ret['data'] = {
            'openid': openid,
        }
        return JsonResponse(ret)

    # encode date
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return json.JSONEncoder.default(self, obj)
    
    # get star list
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

        # save
        item.save()

        # create json
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
    # get openid & activity_id
    openid = request.POST.get('openid')
    activity_id = request.POST.get('activity_id')
    
    # get user
    try: 
        user = User.objects.get(openid = openid)

    except: 
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '取消收藏失败，该用户不存在'
        ret['data'] = {
            'openid': openid,
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # get user & activity
    try: 
        activity = Activity.objects.get(activity_id = activity_id)

    except: 
        ret = {'code': '102', 'msg': None,'data':{}}
        ret['msg'] = '取消收藏失败，该活动不存在'
        ret['data'] = {
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



'''
Part 3
Intro: Functions to save test data
Num: 1
List: 
    - saveTestData(request)
'''

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



'''
Part 5
Intro: Function to operate QRCode
Num: 2
List: 
    - index(request)
'''

def testQRCode(request):
    test_ticket = Ticket.objects.get(ticket_id = 20)

    # create new QRCode
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    url='another_test_qrcode'
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('media/QR/test_qrcode.png')
    test_ticket.QRCode = 'QR/test_qrcode.png'
    test_ticket.save()
    '''
    ERROR_CORRECT_L: 大约7%或更少的错误能被纠正
    ERROR_CORRECT_M:（默认）大约15%或更少的错误能被纠正
    ROR_CORRECT_H:大约30%或更少的错误能被纠正
    '''
    return HttpResponse(test_ticket.QRCode.url)

def logo(request):
    test_ticket = Ticket.objects.get(ticket_id = 20)
    # create new QRCode
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=4,
    )
    url='logo_qrcode'
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert("RGBA")
    icon = Image.open('media/logo.png')
    img_w, img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)
    icon_w, icon_h = icon.size
    if icon_w >size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w,icon_h),Image.ANTIALIAS)
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h), icon)

    img.save('media/QR/test_qrcode.png')
    test_ticket.QRCode = 'QR/test_qrcode.png'
    test_ticket.save()

    return HttpResponse(test_ticket.QRCode.url)



'''
Part 5
Intro: Function to show page for testing net connect
Num: 1
List: 
    - index(request)
'''

def index(request):
    return HttpResponse("Hello! You are at the index page")
