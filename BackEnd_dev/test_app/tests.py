# -*- coding: utf-8 -*-

from django.test import (TestCase, RequestFactory)
from django.test import Client

from .models import (Activity, User, Ticket)
from .views import *

class TestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(user_id=100, 
                            openid='test_openid', 
                            username='test_username', 
                            password='test_password', 
                            )

        self.verify_user = User.objects.create(user_id=200, 
                            openid='verify_test_openid', 
                            username='verify_test_username', 
                            password='verify_test_password', 
                            student_id='2017019999',
                            is_verified=True,
                            )

        self.activity = Activity.objects.create(activity_id=100, 
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

        self.remain_activity = Activity.objects.create(activity_id=200, 
                                title='unit_test_activity2', 
                                image='default/test_image.jpg', 
                                status='正在抢票', 
                                remain=0, 
                                publisher='TECC', 
                                heat=100, 
                                description='测试活动', 
                                time='2020-12-01 12:30:00.000000', 
                                place='大礼堂', 
                                price=100, 
                                )

        ticket = Ticket(ticket_id=100, activity=self.activity, owner=self.user)
        ticket.is_valid = True
        ticket.save()

        invalid_ticket = Ticket(ticket_id=200, activity=self.activity, owner=self.user)
        invalid_ticket.is_valid = False
        invalid_ticket.save()

    # tests for Part 0: init
    def test_init000(self):
        response = self.client.post('/init/', {'code': '023VDKHy0RvEgb19ajLy0ywuHy0VDKHt', 
                                                'info': '{"nickName":"二刺螈螈长","gender":1,"language":"zh_CN","city":"","province":"","country":"China","avatarUrl":"https://wx.qlogo.cn/mmopen/vi_32/YflLdCdbUAliavJbEgGj2NHjiby2SQloD8PYYiamJhAP7ZqVlKZDribWsoRmZz9Q1A7Q1NMJUJ1XYCtgTYOrSKvNiag/132"}'
                                                })

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[9:14], '40029')
 
    def test_verifyUser001(self):
        response = self.client.post('/verifyUser/', {'openid': 'test_openid',
                                                'student_id': '2017010000',
                                                })

        self.assertEqual(response.status_code, 200)

        self.assertEqual(User.objects.get(openid = 'test_openid').student_id, '2017010000')

    def test_verifyUser401(self):
        response = self.client.post('/verifyUser/', {'openid': 'test_openid',
                                                })

        self.assertEqual(response.status_code, 200)
        
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'code': '401', 'msg': '认证失败，无学号', 'data':{'openid': 'test_openid'}}
        )

    def test_verifyUser101(self):
        response = self.client.post('/verifyUser/', {'openid': 'wrong_test_openid',
                                                'student_id': '2017010000',
                                                })

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'code': '101', 'msg': '认证失败，该用户不存在', 'data':{'openid': 'wrong_test_openid'}}
        )

    # tests for Part 1: activity
    def test_getActivityList010(self):
        response = self.client.post('/getActivityList/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '010')

    def test_getActivityInfo011(self):
        response = self.client.post('/getActivityInfo/', {'activity_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '011')

    def test_getActivityInfo211(self):
        response = self.client.post('/getActivityInfo/', {'activity_id': 111})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '211')

    def test_getScrollActivity012(self):
        response = self.client.post('/getScrollActivity/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '012')

    def test_searchEngine013(self):
        response = self.client.post('/searchEngine/', {'line': 'test'})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '013')

    def test_getTimeSortedActivity014(self):
        response = self.client.post('/getTimeSortedActivity/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '014')

    def test_getHeatSortedActivity015(self):
        response = self.client.post('/getHeatSortedActivity/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '015')

    def test_addActivity016(self):
        response = self.client.post('/addActivity/', {'title': '学生节', 
                                                    'price': 111.0, 
                                                    'place': '大礼堂'
                                                    })

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '016')

        self.assertEqual(Activity.objects.get(title = '学生节').place, '大礼堂')
        self.assertEqual(Activity.objects.get(title = '学生节').price, 111)

    # tests for Part 2: ticket
    def test_purchaseTicket020(self):
        response = self.client.post('/purchaseTicket/', {'openid': 'verify_test_openid', 'activity_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '020')

    def test_purchaseTicket120a(self):
        response = self.client.post('/purchaseTicket/', {'openid': 'wrong_test_openid', 'activity_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '120')

    def test_purchaseTicket120b(self):
        response = self.client.post('/purchaseTicket/', {'openid': 'test_openid', 'activity_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '120')

    def test_purchaseTicket220(self):
        response = self.client.post('/purchaseTicket/', {'openid': 'verify_test_openid', 'activity_id': 111})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '220')

    def test_purchaseTicket320a(self):
        response = self.client.post('/purchaseTicket/', {'openid': 'verify_test_openid', 'activity_id': 200})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '320')

    def test_purchaseTicket320b(self):
        self.client.post('/purchaseTicket/', {'openid': 'verify_test_openid', 'activity_id': 100})

        response = self.client.post('/purchaseTicket/', {'openid': 'verify_test_openid', 'activity_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '320')

    def test_refundTicket021(self):
        response = self.client.post('/refundTicket/', {'ticket_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '021')

    def test_refundTicket321a(self):
        response = self.client.post('/refundTicket/', {'ticket_id': 111})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '321')

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'code': '321', 'msg': '退票失败，该票不存在', 'data':{'ticket_id': '111'}}
        )

    def test_refundTicket321b(self):
        response = self.client.post('/refundTicket/', {'ticket_id': 200})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '321')

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'code': '321', 'msg': '退票失败，该票为已退票状态', 'data':{'ticket_id': '200', 'is_valid': False}}
        )

    def test_getTicketList022(self):
        response = self.client.post('/getTicketList/', {'openid': 'test_openid'})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '022')

    def test_getTicketList122(self):
        response = self.client.post('/getTicketList/', {'openid': 'wrong_test_openid'})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '122')

    def test_getTicketInfo023(self):
        response = self.client.post('/getTicketInfo/', {'ticket_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '023')

    def test_getTicketInfo323(self):
        response = self.client.post('/getTicketInfo/', {'ticket_id': 111})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '323')

    # tests for Part 3: star
    def test_starActivity030(self):
        response = self.client.post('/starActivity/', {'openid': 'test_openid', 'activity_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '030')

    def test_starActivity130(self):
        response = self.client.post('/starActivity/', {'openid': 'wrong_test_openid', 'activity_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '130')

    def test_starActivity230(self):
        response = self.client.post('/starActivity/', {'openid': 'test_openid', 'activity_id': 111})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '230')

    def test_deleteStar031(self):
        self.client.post('/starActivity/', {'openid': 'test_openid', 'activity_id': 100})
        response = self.client.post('/deleteStar/', {'openid': 'test_openid', 'activity_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '031')

    def test_deleteStar131(self):
        response = self.client.post('/deleteStar/', {'openid': 'wrong_test_openid', 'activity_id': 100})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '131')

    def test_deleteStar231(self):
        response = self.client.post('/deleteStar/', {'openid': 'test_openid', 'activity_id': 111})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '231')

    def test_getStarList032(self):
        response = self.client.post('/getStarList/', {'openid': 'test_openid'})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '032')

    def test_getStarList132(self):
        response = self.client.post('/getStarList/', {'openid': 'wrong_test_openid'})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '132')

    # tests for Part 4: save test data
    def test_saveTestData(self):
        response = self.client.post('/saveTestData/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.content, encoding='utf8')[10:13], '040')

    # test for Part 5: index page
    def test_index(self):
        response = self.client.get('/index/')

        self.assertEqual(response.content, b'060\nHello! You are at the index page')

    # tests for Part 6: inspector & admin control
    def test_checkTicket(self):
        pass

    def test_applyInspector(self):
        pass

    def test_showAllApply(self):
        pass

    def test_showApplyList(self):
        pass

    def test_showInspedtorList(self):
        pass

    # test for Part 7: admin
    def test_admin(self):
        pass

    def tearDown(self):
        # activity delete
        Activity.objects.filter(activity_id=100).delete()
        Activity.objects.filter(activity_id=200).delete()

        # user delete
        User.objects.filter(user_id=100).delete()
        User.objects.filter(user_id=200).delete()

        # ticket delete
        Ticket.objects.filter(ticket_id=100).delete()
