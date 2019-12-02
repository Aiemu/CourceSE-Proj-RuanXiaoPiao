# Generated by Django 2.2.7 on 2019-12-02 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('activity_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('image', models.ImageField(default='default/test_image.jpg', upload_to='images')),
                ('status', models.CharField(default='正在抢票', max_length=20)),
                ('remain', models.IntegerField(default=100)),
                ('publisher', models.CharField(default='unknown publisher', max_length=30)),
                ('description', models.CharField(default='哎呀，这个活动的介绍文字似乎走丢了...', max_length=1024)),
                ('time', models.DateTimeField(default='2019-10-10 12:30:00')),
                ('place', models.CharField(default='none place', max_length=30)),
                ('price', models.FloatField(default=0.0)),
            ],
            options={
                'db_table': 'Activity',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('openid', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('student_id', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_valid', models.BooleanField(default=False)),
                ('purchaseTime', models.DateTimeField(auto_now_add=True, verbose_name='购票日期')),
                ('activity', models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='test_app.Activity')),
                ('owner', models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='test_app.User')),
            ],
            options={
                'db_table': 'Ticket',
            },
        ),
    ]
