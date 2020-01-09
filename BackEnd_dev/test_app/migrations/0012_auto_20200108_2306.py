# Generated by Django 2.2.7 on 2020-01-08 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0011_auto_20200108_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='inspector_apply_list',
            field=models.ManyToManyField(blank=True, related_name='inspector_apply_list', to='test_app.Activity'),
        ),
        migrations.AlterField(
            model_name='user',
            name='inspector_list',
            field=models.ManyToManyField(blank=True, related_name='inspector_list', to='test_app.Activity'),
        ),
        migrations.AlterField(
            model_name='user',
            name='starred',
            field=models.ManyToManyField(blank=True, related_name='starred', to='test_app.Activity'),
        ),
    ]
