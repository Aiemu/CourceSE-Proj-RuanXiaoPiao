# Generated by Django 2.2.4 on 2019-12-03 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='starred',
            field=models.ManyToManyField(to='test_app.Activity'),
        ),
    ]
