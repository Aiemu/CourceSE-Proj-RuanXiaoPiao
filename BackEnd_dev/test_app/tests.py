# -*- coding: utf-8 -*-

from django.test import (TestCase, RequestFactory)

from .models import (Activity, User, Ticket)
from .views import *

# class ActivityTestCase(TestCase):
#     def setUp(self):
#         Activity.objects.create(activity_id=100, 
#                                 title='unit_test_activity1', 
#                                 image='default/test_image.jpg', 
#                                 status='正在抢票', 
#                                 remain=100, 
#                                 publisher='TECC', 
#                                 heat=100, 
#                                 description='测试活动', 
#                                 time='2020-12-01 12:30:00.000000', 
#                                 place='西操', 
#                                 price=100, 
#                                 )
    
#     def test_init(self):
#         activity = Activity.objects.get(activity_id=100)
    
#     def tearDown(self):
#         Activity.objects.filter(activity_id=100).delete()

# class UserTestCase(TestCase):
#     def setUp(self):
#         User.objects.create(user_id=100, 
#                             openid='test_openid', 
#                             username='test_username', 
#                             password='test_password', 
#                             student_id='2017010000', 
#                             is_verified=1
#                             )
    
#     def test_init(self):
#         user = User.objects.get(user_id=100)
    
#     def tearDown(self):
#         User.objects.filter(user_id=100).delete()

class TicketTestCase(TestCase):
    def setUp(self):
        Activity.objects.create(activity_id=100, 
                                title='unit_test_activity1', 
                                image='default/test_image.jpg', 
                                status='正在抢票', 
                                remain=100, 
                                publisher='TECC', 
                                heat=100, 
                                description='测试活动', 
                                time='2020-12-01 12:30:00.000000', 
                                place='西操', 
                                price=100, 
                                )
        activity = Activity.objects.get(activity_id=100)

        User.objects.create(user_id=100, 
                            openid='test_openid', 
                            username='test_username', 
                            password='test_password', 
                            student_id='2017010000', 
                            is_verified=1
                            )
        user = User.objects.get(user_id=100)

        ticket = Ticket(owner = user, activity = activity)

        # verify
        ticket.is_valid = True
        print('ticket.ticket_id: ')
        print(ticket.owner_id)

        # save
        ticket.save()
    
    def test_init(self):
        ticket = Ticket.objects.get(ticket_id=0)
    
    def tearDown(self):
        Ticket.objects.filter(ticket_id=0).delete()