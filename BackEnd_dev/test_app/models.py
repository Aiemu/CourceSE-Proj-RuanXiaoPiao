from django.db import models
from datetime import datetime

class Activity(models.Model):
    activity_id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 30)
    image = models.ImageField(upload_to = 'images', default = 'default/test_image.jpg')
    status = models.CharField(max_length = 20, default = '正在抢票')
    remain = models.IntegerField(default = 100)
    publisher = models.CharField(max_length = 30, default = 'unknown publisher')
    description = models.CharField(max_length = 1024, default = '哎呀，这个活动的介绍文字似乎走丢了...')
    time = models.DateTimeField(default = datetime.now)
    place = models.CharField(max_length = 30, default = 'none place')
    price = models.FloatField(default = 0.0)

    heat = models.FloatField(default = 50.0) # 活动热度
    scan_change = models.FloatField(default = 0.02) # 浏览时增加的热度
    star_change = models.FloatField(default = 0.5) # 关注/取关时的热度变化
    purchase_change = models.FloatField(default = 2.0) # 购买/退票时的热度变化
    # arrive_change = models.FloatField(default = 2.5) # 到场时的热度变化
    # max_heat = models.FloatField(default = 1000)
    min_heat = models.FloatField(default = 0) # 活动过期后置为最低热度
    
    class Meta:
        db_table = 'Activity'

class User(models.Model):
    # basic info
    user_id = models.AutoField(primary_key = True)
    openid = models.CharField( max_length = 30)
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    student_id =  models.CharField(max_length = 10)
    starred = models.ManyToManyField(Activity)

    # varify info
    is_verified = models.BooleanField(default=False) # 学号登录验证接口

    class Meta:
        db_table = 'User'

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key = True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, default = '')
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING, default = '')
    is_valid = models.BooleanField(default=False) # 仅表示是否退票
    purchaseTime = models.DateTimeField('购票日期', auto_now_add = True) # PS:auto_now_add使之为readonly。若需修改puchaseTime，则此处应改用default = timezone.now
                                                                    # WARMNING:修改含auto_now或auto_now_add的字段时，需先改为default = 'xxxx-xx-xx xx:xx:xx'并完成一次迁移
    QRCode = models.ImageField(upload_to = 'QR', default = 'QR/default.png')
    is_checked = models.BooleanField(default=False)

    class Meta:
        db_table = 'Ticket'
