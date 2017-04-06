# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20170403_0309'),
        ('df_goods', '0002_auto_20170403_0341'),
    ]

    operations = [
        migrations.CreateModel(
            name='shopcart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goodCount', models.IntegerField()),
                ('goodinfo', models.ForeignKey(to='df_goods.GoodsInfo')),
                ('userinfo', models.ForeignKey(to='df_user.userInfo')),
            ],
        ),
    ]
