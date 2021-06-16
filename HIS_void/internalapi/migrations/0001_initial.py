# Generated by Django 3.1.7 on 2021-06-16 17:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('trade_no', models.CharField(max_length=64, primary_key=True, serialize=False, verbose_name='订单号')),
                ('total_amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='总订单费用')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='HIS系统创建订单的时间。', verbose_name='订单时间')),
                ('item_type', models.IntegerField(choices=[(0, '挂号'), (1, '检查检验'), (2, '手术'), (3, '处方'), (4, '出院结算')], help_text='不同项目类型对应着不同的表，例如检查检验表、手术信息表、处方表等。', verbose_name='项目类型')),
                ('item_name', models.CharField(max_length=64, verbose_name='项目名称')),
                ('item_pk', models.CharField(help_text="以'-'连接的主键值。例如，该条缴费记录对应一个患者检查检验，需要主键 (reg_id, test_id) 来索引。", max_length=64, verbose_name='记录主键')),
                ('is_pay', models.IntegerField(choices=[(0, '未缴费'), (1, '缴费成功'), (2, '缴费失败')], default=0, help_text='0代表未缴费，1代表成功缴费, 2代表缴费失败', verbose_name='缴费状态')),
            ],
            options={
                'verbose_name': '缴费记录',
                'verbose_name_plural': '缴费记录',
            },
        ),
    ]
