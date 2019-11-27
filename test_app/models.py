from django.db import models

# Create your models here.

class User(models.Model):
    # basic info
    user_id = models.AutoField(primary_key = True) # autofield自动改变
    openid = models.CharField( max_length = 30)
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    student_id =  models.CharField(max_length = 10)

    # varify info
    # user_permissions = models.ManyToManyField() 
    # is_verified = models.BooleanField() # 学号登录验证接口

    # 指定表名,否则默认为test_app_User
    class Meta:
        db_table = 'User'

class Activity(models.Model):
    activity_id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 30)
    # image = models.ImageField() # TODO
    # status = models.ChoiceField() # TODO 每次获取活动信息则更新
    # remain = models.IntegerField(default = 0) # TODO 每生成一张票++，每退一张--
    # publisher = models.CharField() # TODO
    # heat = models.FloatField() # TO BE DEFINED
    # description = models.CharField() # TODO
    time = models.CharField(max_length = 30, default = '0000.00.00 00:00') # TODO
    place = models.CharField(max_length = 30, default = 'none place')
    price = models.FloatField(default = 0.0)
    # keywords = models.ManyToManyField() # 搜索 分词 关键词
    
    class Meta:
        db_table = 'Activity'

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key = True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, default = '')
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING, default = '')
    is_valid = models.BooleanField(default=False)
    # purchaseTime = models.DatetimeField() # TODO 生成票时设置
    # QRCode = models.ImageField() # TODO
    # is_checked = models.BooleanField()

    class Meta:
        db_table = 'Ticket'
