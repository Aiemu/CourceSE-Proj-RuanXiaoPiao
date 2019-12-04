from django.db import models
from datetime import datetime

class Activity(models.Model):
    activity_id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 30)
    image = models.ImageField(upload_to = 'images', default = 'default/test_image.jpg')
    status = models.CharField(max_length = 20, default = '正在抢票')
    remain = models.IntegerField(default = 100)
    publisher = models.CharField(max_length = 30, default = 'unknown publisher')
    
    heat = models.FloatField(default = 0.0) # TO BE DEFINED
    description = models.CharField(max_length = 1024, default = '哎呀，这个活动的介绍文字似乎走丢了...')
    time = models.DateTimeField(default = datetime.now)
    place = models.CharField(max_length = 30, default = 'none place')
    price = models.FloatField(default = 0.0)
    # keywords = models.() # 搜索 分词 关键词
    
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
    # user_permissions = models.ManyToManyField() 
    # is_verified = models.BooleanField() # 学号登录验证接口

    # 指定表名,否则默认为test_app_User
    class Meta:
        db_table = 'User'

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key = True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, default = '')
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING, default = '')
    is_valid = models.BooleanField(default=False) # 仅表示是否退票
    purchaseTime = models.DateTimeField('购票日期', auto_now_add = True) # PS:auto_now_add使之为readonly。若需修改puchaseTime，则此处应改用default = timezone.now
                                                                    # WARMNING:修改含auto_now或auto_now_add的字段时，需先改为default = 'xxxx-xx-xx xx:xx:xx'并完成一次迁移
    # QRCode = models.ImageField() # TODO
    # is_checked = models.BooleanField()

    class Meta:
        db_table = 'Ticket'

class HeatMode(models.Model):
    mode_id = models.AutoField(primary_key = True)
    # mode_class = models.CharField(max_length = 20, default = '新增类型')
    origin = models.FloatField(default = 50.0)
    scan_change = models.FloatField(default = 0.2)
    star_change = models.FloatField(default = 0.5)
    unstar_change = models.FloatField(default = -0.5)
    buy_change = models.FloatField(default = 2.0)
    refund_change = models.FloatField(default = -2.0)
    arrive_change = models.FloatField(default = 2.5)
    over_change = models.FloatField(default = -100)
    max_heat = models.FloatField(default = 1000)
    min_heat = models.FloatField(default = 0)
    
    class Meta:
        db_table = 'HeatMode'