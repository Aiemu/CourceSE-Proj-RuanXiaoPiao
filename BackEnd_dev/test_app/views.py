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
import random
import string

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
Num: 2
List: 
    - init(request)
    - verifyUser(request)
'''

@api_view(['POST'])

def init(request):
    '''
    Intro: 
        get openid, add user into database
    Args(request): 
        code(str): used as certificate to get openid
        user_info(str): used to enrich user's info in database
    Returns:    
        {code: 000, msg: 授权成功, data: {jwt(str), openid(str), nickname(str)}}
    '''
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
    ret = {'code': '000', 'msg': None, 'data':{}}
    ret['msg'] = '授权成功'
    ret['data'] = {
        'jwt': jwt,
        'openid': user.openid,
        'nickname': user.username
    }
    return JsonResponse(ret)

def verifyUser(request):
    '''
    Intro: 
        update user's is_verified
    Args(request): 
        openid(str): used to identify user
        student_id: flag to verify
    Returns: 
        {code: 101, msg: 认证失败，该用户不存在, data: {openid(str)}}
        {code: 001, msg: 认证成功, data: {openid(str), student_id(str)}}
    '''
    # get openid & student_id
    openid = request.POST.get('openid')
    student_id = request.POST.get('student_id')

    if student_id == None:
        ret = {'code': '401', 'msg': None, 'data':{}}
        ret['msg'] = '认证失败，无学号'
        ret['data'] = {
            'openid': openid,
        }
        return JsonResponse(ret)

    # get user
    try: 
        user = User.objects.get(openid = openid)
    except:
        ret = {'code': '101', 'msg': None, 'data':{}}
        ret['msg'] = '认证失败，该用户不存在'
        ret['data'] = {
            'openid': openid,
        }
        return JsonResponse(ret)
    
    # update user
    user.is_verified = True
    user.student_id = student_id

    # save
    user.save()

    # ret msg
    ret = {'code': '001', 'msg': None, 'data':{}}
    ret['msg'] = '认证成功'
    ret['data'] = {
        'openid': openid,
        'student_id': student_id,
    }
    return JsonResponse(ret)



'''
Part 1
Intro: Functions to operate activity
Num: 7
List: 
    - getActivityList(request)
    - getActivityInfo(request)
    - getScrollActivity(request)
    - searchEngine(request)
    - getTimeSortedActivity(request)
    - getHeatSortedActivity(request)
    - addActivity(request)
'''

def getActivityList(request): 
    '''
    Intro: 
        return all activities in database
    Args(request): 
        None
    Returns: 
        {code: 010, msg: 获取活动列表成功, data: {activityList(list)}}
    '''
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
    ret = {'code': '010', 'msg': None, 'data':{}}
    ret['msg'] = '获取活动列表成功'
    ret['data'] = {
        'activityList': retList,
    }
    return JsonResponse(ret)

def getActivityInfo(request): 
    '''
    Intro: 
        get the details of an activity with activity_id
    Args(request): 
        activity_id(int): used to identify activity
    Returns: 
        {code: 211, msg: 获取活动详情失败，该活动不存在, data: {activity_id(int)}}
        {code: 011, msg: 活动详情获取成功, data: {activity_id(int), title(str), 
                                            image(str), status(str), remain(int), 
                                            publisher(str), description(str), 
                                            time(date), place(str), price(double), 
                                            heat(double)}}
    '''
    # get activity_id
    activity_id = request.POST.get('activity_id')

    # get user & activity
    try: 
        activity = Activity.objects.get(activity_id = activity_id)
    except:
        ret = {'code': '211', 'msg': None, 'data':{}}
        ret['msg'] = '获取活动详情失败，该活动不存在'
        ret['data'] = {
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # 浏览活动详情，改变活动热度
    activity.heat += activity.scan_change
    activity.save()

    # ret msg
    ret = {'code': '011', 'msg': None, 'data':{}}
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
    '''
    Intro: 
        return top 5 activities(rank with heat)
    Args(request): 
        None
    Returns: 
        {code: 012, msg: 获取滚图成功, data: {activityList(list)}}
    '''
    # encode date
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return json.JSONEncoder.default(self, obj)
    
    actList = Activity.objects.filter(status = '正在抢票').order_by('-heat')
    retList = []

    # count num of ret
    count = 0

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
        if count < 5:
            i = {
                'activity_id': item.activity_id, 
                'image': 'http://62.234.50.47' + item.image.url,
                'heat': item.heat,
            }
            iJson = json.dumps(i, cls = DateEncoder)
            retList.append(iJson)
            count += 1
        else:
            break
    
    # ret msg
    ret = {'code': '012', 'msg': None, 'data':{}}
    ret['msg'] = '获取滚图成功'
    ret['data'] = {
        'activityList': retList,
    }
    return JsonResponse(ret)

def searchEngine(request): 
    '''
    Intro: 
        cut line into words, use words to compare with activitise' info to get suitable activities
    Args(request): 
        line(str): what user typed in edit-line
    Returns: 
        {code: 013, msg: 搜索成功, data: {actList(list)}}
    '''
    # encode date
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return json.JSONEncoder.default(self, obj)

    # search line
    line = request.POST.get('line')

    # cut word
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

        # save
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
    ret = {'code': '013', 'msg': None, 'data':{}}
    ret['msg'] = '搜索成功'
    ret['data'] = {
        'actList': retactList,
    }
    return JsonResponse(ret)

def getTimeSortedActivity(request): 
    '''
    Intro: 
        return activities sorted by time
    Args(request): 
        None
    Returns: 
        {code: 014, msg: 获取按时间排序的活动列表成功, data: {activityList(list)}}
    '''
    # encode date
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return json.JSONEncoder.default(self, obj)
    
    # get list
    actList = Activity.objects.filter(min_heat=0).order_by('-time')
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
    ret = {'code': '014', 'msg': None, 'data':{}}
    ret['msg'] = '获取按时间排序的活动列表成功'
    ret['data'] = {
        'activityList': retList,
    }
    return JsonResponse(ret)

def getHeatSortedActivity(request): 
    '''
    Intro: 
        return activities sorted by heat
    Args(request): 
        None
    Returns: 
        {code: 015, msg: 获取按热度排序的活动列表成功, data: {activityList(list)}}
    '''
    # encode date
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return json.JSONEncoder.default(self, obj)
    
    # get list
    actList = Activity.objects.filter(min_heat=0).order_by('-heat')
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
    ret = {'code': '015', 'msg': None, 'data':{}}
    ret['msg'] = '获取按热度排序的活动列表成功'
    ret['data'] = {
        'activityList': retList,
    }
    return JsonResponse(ret)

def addActivity(request): 
    '''
    Intro: 
        add activity into database
    Args(request): 
        title(str): activity title
        price(double): activity price
        place(str): activity place
        time(date): activity time
    Returns: 
        {code: 015, msg: 获取按热度排序的活动列表成功, data: {activityList(list)}}
    '''
    title = request.POST.get('title')
    price = request.POST.get('price')
    place = request.POST.get('place')
    time = request.POST.get('time')
    # TODO



'''
Part 2
Intro: Functions to operate ticket
Num: 5
List: 
    - purchaseTicket(request)
    - refundTicket(request)
    - getTicketList(request)
    - getTicketInfo(request)
    - checkTicket(request)
'''

def purchaseTicket(request): 
    '''
    Intro: 
        create new ticket and add it into user's ticket list
    Args(request): 
        openid(str): used to identify user, saved in the cache of front-end
        activity_id: used to identify activity
    Returns: 
        {code: 120, msg: 购票失败，该用户不存在, data: {openid(str), activity_id(int)}}
        {code: 120, msg: 购票失败，该用户未认证, data: {openid(str), activity_id(int)}}
        {code: 220, msg: 购票失败，该活动不存在, data: {openid(str), activity_id(int)}}
        {code: 320, msg: 购票失败，余票不足, data: {openid(str), activity_id(int), remain(int)}}
        {code: 320, msg: 购票失败，票已存在, data: {openid(str), activity_id(int), remain(int)}}
        {code: 020, msg: 购票成功, data: {openid(str), activity_id(int), remain(int)}}
    '''
    # get openid & activity_id
    openid = request.POST.get('openid')
    activity_id = request.POST.get('activity_id')
    
    # get user & activity
    try: 
        user = User.objects.get(openid = openid)
    except:
        ret = {'code': '120', 'msg': None, 'data':{}}
        ret['msg'] = '购票失败，该用户不存在'
        ret['data'] = {
            'openid': openid,
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # check if user is verified
    if not user.is_verified: 
        ret = {'code': '120', 'msg': None, 'data':{}}
        ret['msg'] = '购票失败，该用户未认证'
        ret['data'] = {
            'openid': openid,
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # get activity
    try: 
        activity = Activity.objects.get(activity_id = activity_id)
    except:
        ret = {'code': '220', 'msg': None, 'data':{}}
        ret['msg'] = '购票失败，该活动不存在'
        ret['data'] = {
            'openid': openid,
            'activity_id': activity_id,
        }
        return JsonResponse(ret)

    # check remain
    if activity.remain <= 0:
        # ret msg
        ret = {'code': '320', 'msg': None, 'data':{}}
        ret['msg'] = '购票失败，余票不足'
        ret['data'] = {
            'openid': openid,
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
                    ret = {'code': '320', 'msg': None, 'data':{}}
                    ret['msg'] = '购票失败，票已存在'
                    ret['data'] = {
                        'openid': openid,
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
        
        # verify ticket
        ticket.is_valid = True

        # define QRCode mode
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=8,
            border=4,
        )
        # get random mark as part of the url
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        url = "RuanXiaoPiao_Unique: "
        for i in range(3):
            url = url + random.choice(letters) + " + "
        url = url + str(user.user_id) + " + " + str(activity.activity_id)
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

        img.save('media/QR/' + str(user.user_id) + '_' + str(activity.activity_id) +'.png')
        ticket.QRCode = 'QR/' + str(user.user_id) + '_' + str(activity.activity_id) +'.png'

        # save ticket
        ticket.save()
        
        # ret msg
        ret = {'code': '020', 'msg': None, 'data':{}}
        ret['msg'] = '购票成功'
        ret['data'] = {
            'openid': openid,
            'activity_id': activity.activity_id,
            'remain': activity.remain,
        }
        return JsonResponse(ret)

def refundTicket(request): 
    '''
    Intro: 
        update ticket's is_valid into false
    Args(request): 
        ticket_id(int): used to identify ticket
    Returns: 
        {code: 321, msg: 退票失败，该票不存在, data: {ticket_id(int)}}
        {code: 021, msg: 退票成功, data: {ticket_id(int), is_valid(bool)}}
        {code: 321, msg: 退票失败，该票为已退票状态, data: {ticket_id(int), is_valid(bool)}}
    '''
    # get ticket_id
    ticket_id = request.POST.get('ticket_id')

    # get activity
    try: 
        ticket = Ticket.objects.get(ticket_id = ticket_id)
        activity = ticket.activity
    except: 
        # ret msg
        ret = {'code': '321', 'msg': None, 'data':{}}
        ret['msg'] = '退票失败，该票不存在'
        ret['data'] = {
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
        ret = {'code': '021', 'msg': None, 'data':{}}
        ret['msg'] = '退票成功'
        ret['data'] = {
            'ticket_id': ticket_id,
            'is_valid': ticket.is_valid,
        }

    else:
        # ret msg
        ret = {'code': '321', 'msg': None, 'data':{}}
        ret['msg'] = '退票失败，该票为已退票状态'
        ret['data'] = {
            'ticket_id': ticket_id,
            'is_valid': ticket.is_valid,
        }
    return JsonResponse(ret)

def getTicketList(request): 
    '''
    Intro: 
        return user's all tickets, include refunded ones
    Args(request): 
        openid: used to identify user
    Returns: 
        {code: 122, msg: 获取已购票列表失败，该用户不存在, data: {openid(str)}}
        {code: 022, msg: 获取已购票列表成功, data: {openid(str), ticketList(list)}}
    '''
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
        ret = {'code': '122', 'msg': None, 'data':{}}
        ret['msg'] = '获取已购票列表失败，该用户不存在'
        ret['data'] = {
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
            'ticket_status': item.is_valid,
            'activity_status': item.activity.status,
            'activity_image': 'http://62.234.50.47' + item.activity.image.url,
            'title': item.activity.title,
            'time': item.activity.time,
            'place': item.activity.place,
            'price': item.activity.price,
            'heat': item.activity.heat,
        }
        iJson = json.dumps(i, cls = DateEncoder)
        retList.append(iJson)

    # ret msg
    ret = {'code': '022', 'msg': None, 'data':{}}
    ret['msg'] = '获取已购票列表成功'
    ret['data'] = {
        'openid': openid,
        'ticketList': retList,
    }
    return JsonResponse(ret)

def getTicketInfo(request): 
    '''
    Intro: 
        get ticket's info from database and return
    Args(request): 
        ticket_id(int): used to identify ticket
    Returns: 
        {code: 323, msg: 获取票详情失败，该票不存在, data: {ticket_id(int)}}
        {code: 023, msg: 获取票详情成功, data: {ticket_id(int), owner(str), title(str), 
                                            price(double), place(str), heat(double), 
                                            tic_time(date), act_time(date), is_valid(bool), 
                                            QRCode(image)}}
    '''
    # get ticket_id
    ticket_id = request.POST.get('ticket_id')

    # get ticket
    try:
        ticket = Ticket.objects.get(ticket_id = ticket_id)
    except:
        ret = {'code': '323', 'msg': None, 'data':{}}
        ret['msg'] = '获取票详情失败，该票不存在'
        ret['data'] = {
            'ticket_id': ticket_id,
        }
        return JsonResponse(ret)

    # ret msg
    ret = {'code': '023', 'msg': None, 'data':{}}
    ret['msg'] = '获取票详情成功'
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
        'QRCode': 'http://62.234.50.47' + ticket.QRCode.url,
    }
    return JsonResponse(ret)

def checkTicket(request): 
    '''
    Intro: 
        check ticket in check-ticket end
    Args(request): 
        ticket_id(int)
    Returns: 
        {code: 324, msg: 检票失败，该票不存在, data: {ticket_id(int)}}
        {code: 224, msg: 检票失败，该活动已结束, data: {ticket_id(int)}}
        {code: 324, msg: 检票失败，该票已使用, data: {ticket_id(int)}}
        {code: 024, msg: 检票成功, data: {ticket_id(int), student_id(str), time(date), place(str)}}
    '''
    # get ticket info
    user_id = request.POST.get('user_id')
    activity_id = request.POST.get('activity_id')

    # get ticket
    try:
        tickets = Ticket.objects.all()
        found = False
        for item in tickets:
            if item.owner.user_id == user_id:
                if item.activity.activity_id == activity_id:
                    found = True
                    ticket = item
                break

        if not found:
            # ret msg
            ret = {'code': '324', 'msg': None, 'data':{}}
            ret['msg'] = '检票失败，该票不存在'
            ret['data'] = {
                'ticket_id': ticket_id
            }
            return JsonResponse(ret)
        else:
            # check time
            if ticket.activity.status == u'已结束': 
                # ret msg
                ret = {'code': '224', 'msg': None, 'data':{}}
                ret['msg'] = '检票失败，该活动已结束'
                ret['data'] = {
                    'ticket_id': ticket_id,
                }
                return JsonResponse(ret)

            # check ticket
            if ticket.is_checked: 
                # ret msg
                ret = {'code': '324', 'msg': None, 'data':{}}
                ret['msg'] = '检票失败，该票已使用'
                ret['data'] = {
                    'ticket_id': ticket_id,
                }
                return JsonResponse(ret)

            # update
            ticket.is_checked = True

            # save
            ticket.save()

            # ret msg
            ret = {'code': '024', 'msg': None, 'data':{}}
            ret['msg'] = '检票成功'
            ret['data'] = {
                'ticket_id': ticket_id, 
                'surdent_id': ticket.owner.student_id, 
                'time': ticket.activity.time, 
                'palce': ticket.activity.place,
            }
            return JsonResponse(ret)

    except Exception as e:
        # # 由于try中已包含几乎所有情况，出现的except按照查无此票处理
        # # ret msg
        # ret = {'code': '324', 'msg': None, 'data':{}}
        # ret['msg'] = '检票失败，该票不存在'
        # ret['data'] = {
        #     'ticket_id': ticket_id
        # }
        # return JsonResponse(ret)
        return JsonResponse(e)

'''
Part 3
Intro: Functions to operate star
Num: 3
List: 
    - starActivity(request)
    - deleteStar(request)
    - getStarList(request)
'''

def starActivity(request): 
    '''
    Intro: 
        add activity into user's star list
    Args(request): 
        openid(str): used to identify user
        activity_id(int): used to identify activity
    Returns: 
        {code: 130, msg: 收藏失败，该用户不存在, data: {openid(str), activity_id(int)}}
        {code: 230, msg: 收藏失败，该活动不存在, data: {openid(str), activity_id(int)}}
        {code: 030, msg: 收藏成功, data: {openid(str), activity_id(int)}}
    '''
    # get openid & activity_id
    openid = request.POST.get('openid')
    activity_id = request.POST.get('activity_id')
    
    # get user
    try: 
        user = User.objects.get(openid = openid)

    except:
        # ret msg
        ret = {'code': '130', 'msg': None, 'data':{}}
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
        ret = {'code': '230', 'msg': None, 'data':{}}
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
    ret = {'code': '030', 'msg': None, 'data':{}}
    ret['msg'] = '收藏成功'
    ret['data'] = {
        'openid': openid,
        'activity_id': activity.activity_id,
    }
    return JsonResponse(ret)

def deleteStar(request): 
    '''
    Intro: 
        delete activity from user's star list
    Args(request): 
        openid(str): used to identify user
        activity_id: used to identify activity
    Returns: 
        {code: 131, msg: 取消收藏失败，该用户不存在, data: {openid(str), activity_id(int)}}
        {code: 231, msg: 取消收藏失败，该活动不存在, data: {openid(str), activity_id(int)}}
        {code: 031, msg: 取消收藏成功, data: {openid(str), activity_id(int)}}
    '''
    # get openid & activity_id
    openid = request.POST.get('openid')
    activity_id = request.POST.get('activity_id')
    
    # get user
    try: 
        user = User.objects.get(openid = openid)

    except: 
        ret = {'code': '131', 'msg': None, 'data':{}}
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
        ret = {'code': '231', 'msg': None, 'data':{}}
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
    ret = {'code': '031', 'msg': None, 'data':{}}
    ret['msg'] = '取消收藏成功'
    ret['data'] = {
        'openid': openid,
        'activity_id': activity_id,
    }
    return JsonResponse(ret)

def getStarList(request): 
    '''
    Intro: 
        return user's star list
    Args(request): 
        openid(str): used to identify user
    Returns: 
        {code: 132, msg: 获取收藏列表失败，该用户不存在, data: {openid(str)}}
        {code: 032, msg: 获取收藏列表成功, data: {activityList(list)}}
    '''
    # get openid
    openid = request.POST.get('openid')
    
    # get user
    try: 
        user = User.objects.get(openid = openid)
    except:
        ret = {'code': '132', 'msg': None, 'data':{}}
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
    ret = {'code': '032', 'msg': None, 'data':{}}
    ret['msg'] = '获取收藏列表成功'
    ret['data'] = {
        'activityList': retList,
    }
    return JsonResponse(ret)

'''
Part 4
Intro: Functions to save test data
Num: 1
List: 
    - saveTestData(request)
'''

# 初始化测试数据库
def saveTestData(request): 
    '''
    Intro: 
        save some data into database
    Args(request): 
        None
    Returns: 
        {code: 050, msg: 保存成功, data: {newUser(str), newActivity(list)}}
    '''
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
    ret = {'code': '050', 'msg': None, 'data':{}}
    ret['msg'] = '保存成功'
    ret['data'] = {
        'newUser': user.openid,
        'newActivity': [activity1.title, activity2.title]
        # 'newTicket': ticket.ticket_id,
    }
    return JsonResponse(ret)

'''
Part 5
Intro: Function to show page for testing net connect
Num: 1
List: 
    - index(request)
'''

def index(request): 
    '''
    Intro: 
        Used to test net connection
    Args(request): 
        None
    Returns: 
        None
    '''
    return HttpResponse("060\nHello! You are at the index page")

# def getTwo(request):
#     try:
#         tickets = Ticket.objects.all()
#         checked = False
#         for ticket in tickets:
#             if ticket.owner.user_id == 4:
#                 if ticket.activity.activity_id == 5:
#                     checked = True
#                 break
#         if checked:
#             return HttpResponse("getTwo_Found")
#         else:
#             return HttpResponse("getTwo_NotFound")
#     except:
#         return HttpResponse("getTwo_NotCheck")