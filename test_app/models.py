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
    # is_verified = models.BooleanField()

    # tickets info
    # tickets = models.(ListField?)

    # 指定表名,否则默认为test_app_User
    class Meta:
        db_table = 'User'

class Activity(models.Model):
    activity_id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 30)
    # image = models.ImageField()
    # status = models.ChoiceField()
    # remain = models.IntegerField(default = 0)
    # publisher = models.CharField()
    # heat = models.FloatField()
    # description = models.CharField()
    time = models.CharField(max_length = 30, default = '0000.00.00 00:00') # TODO
    place = models.CharField(max_length = 30, default = 'none place')
    price = models.FloatField(default = 0.0)
    # keywords = models.ManyToManyField()
    
    class Meta:
        db_table = 'Activity'

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key = True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, default = '')
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING, default = '')
    # price = models.FloatField()
    is_valid = models.BooleanField(default=False)
    # is_checked = models.BooleanField()

    class Meta:
        db_table = 'Ticket'
