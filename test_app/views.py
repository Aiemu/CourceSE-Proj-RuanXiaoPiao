import hashlib
import json
import requests
import rest_framework
import pymysql.cursors
import pymysql
import pandas as pds

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django_redis import get_redis_connection
from .models import User, Activity, Ticket
from .serializers import UserSerializer

# @api_view(['POST'])

# from code to session
def init(request):
    # appid & secret
    appid = 'wx4d722f66e80e339e'
    appsecret = 'c9e072d2c443a1e2680f31db7a73ff72'

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
    user, created = User.objects.get_or_create(openid=openid)

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

def getList(request):
    actList = Activity.objects.all()
    retList = []
    for item in actList:
        i = {
            'activity_id': item.activity_id, 
            'title': item.title, 
            'time': item.time, 
            'place': item.place, 
            'price': item.price
        }
        iJson = json.dumps(i)
        retList.append(iJson)
        
    # ret msg
    ret = {'code': '001', 'msg': None,'data':{}}
    ret['msg'] = '获取活动列表成功'
    ret['data'] = {
        'activityList': retList,
    }
    return JsonResponse(ret)

def purchaseTicket(request):
    # appid & secret
    appid = 'wx4d722f66e80e339e'
    appsecret = 'c9e072d2c443a1e2680f31db7a73ff72'

    # code & userinfo
    js_code = request.POST.get('code')
    activity_id = request.POST.get('activity_id')

    print('actid: ', request)

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
    user, created = User.objects.get_or_create(openid = openid)
    activity, created = Activity.objects.get_or_create(activity_id = activity_id)

    # new ticket
    ticket = Ticket(owner = user, activity = activity)

    ticket.save()

    # ret msg
    ret = {'code': '002', 'msg': None,'data':{}}
    ret['msg'] = '购票成功'
    ret['data'] = {
        'user': user.username,
        'activity_id': activity_id,
    }
    return JsonResponse(ret)

def saveTestData(request):
    # test data for user
    openid = 'hello'

    user, created = User.objects.get_or_create(openid = openid)
    user_str = str(UserSerializer(user).data)

    user.username = 'testName'
    user.password = openid

    user.save()

    # test data for acvivity
    title = 'Test activity 2'
    activity, created = Activity.objects.get_or_create(title = title)

    activity.time = '2019.08.27 9:00'
    activity.place = '大礼堂'
    activity.price = 123

    activity.save()

    # test data for ticket
    ticket = Ticket(owner = user, activity = activity)

    ticket.save()
    
    # ret msg
    ret = {'code': '003', 'msg': None,'data':{}}
    ret['msg'] = '保存成功'
    ret['data'] = {
        'newUser': user.username,
        'newActivity': activity.title,
        'newTicket': ticket.ticket_id,
    }
    return JsonResponse(ret)


def index(request):
    return HttpResponse("Hello world! You are at the test_app index.")
