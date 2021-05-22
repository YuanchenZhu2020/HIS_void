# Generated by Django 3.1.7 on 2021-05-17 07:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentInfo',
            fields=[
                ('purchase_date', models.DateField(auto_created=True, editable=False, verbose_name='采购日期')),
                ('equipment_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='设备全局编号')),
                ('equipment_model', models.CharField(max_length=20, verbose_name='设备型号')),
                ('start_using', models.DateField(verbose_name='启用日期')),
                ('lifetime', models.PositiveIntegerField(verbose_name='理论使用寿命')),
            ],
            options={
                'verbose_name': '设备信息',
                'verbose_name_plural': '设备信息',
            },
        ),
        migrations.CreateModel(
            name='EquipmentTypeInfo',
            fields=[
                ('eq_type_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='设备类型编号')),
                ('eq_type_name', models.CharField(max_length=100, verbose_name='设备类型名称')),
            ],
            options={
                'verbose_name': '设备类型信息',
                'verbose_name_plural': '设备类型信息',
            },
        ),
        migrations.CreateModel(
            name='PatientTestItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_time', models.DateTimeField(auto_created=True, editable=False, verbose_name='开具时间')),
                ('test_id', models.PositiveIntegerField(help_text='A病人第X次挂号的第i项检验', verbose_name='检验序号')),
                ('test_results', models.TextField(blank=True, max_length=400, verbose_name='检验结果')),
                ('payment_status', models.BooleanField(default=False, verbose_name='缴费状态')),
            ],
            options={
                'verbose_name': '患者检验项目',
                'verbose_name_plural': '患者检验项目',
            },
        ),
        migrations.CreateModel(
            name='TestItemType',
            fields=[
                ('inspect_type_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='检验项目类型编号')),
                ('inspect_type_name', models.CharField(max_length=30, verbose_name='检验项目类型名称')),
            ],
            options={
                'verbose_name': '检验项目类型',
                'verbose_name_plural': '检验项目类型',
            },
        ),
        migrations.CreateModel(
            name='TestItem',
            fields=[
                ('inspect_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='检验项目编号')),
                ('inspect_name', models.CharField(max_length=30, verbose_name='检验项目名称')),
                ('inspect_price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='检验价格')),
                ('inspect_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='laboratory.testitemtype', verbose_name='检验项目类型')),
            ],
            options={
                'verbose_name': '检验项目',
                'verbose_name_plural': '检验项目',
            },
        ),
    ]
