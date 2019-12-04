# Generated by Django 2.2.7 on 2019-12-04 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0003_auto_20191204_0730'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeatMode',
            fields=[
                ('mode_id', models.AutoField(primary_key=True, serialize=False)),
                ('origin', models.FloatField(default=50.0)),
                ('scan_change', models.FloatField(default=0.2)),
                ('star_change', models.FloatField(default=0.5)),
                ('unstar_change', models.FloatField(default=-0.5)),
                ('buy_change', models.FloatField(default=2.0)),
                ('refund_change', models.FloatField(default=-2.0)),
                ('arrive_change', models.FloatField(default=2.5)),
                ('over_change', models.FloatField(default=-100)),
                ('max_heat', models.FloatField(default=1000)),
                ('min_heat', models.FloatField(default=0)),
            ],
        ),
    ]
