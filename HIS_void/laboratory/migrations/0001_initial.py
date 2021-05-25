# Generated by Django 3.1.7 on 2021-05-25 05:42

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
                ('equipment_id', models.BigAutoField(help_text='设备全局编号', primary_key=True, serialize=False, verbose_name='设备编号')),
                ('equipment_model', models.CharField(max_length=20, verbose_name='设备型号')),
                ('purchase_date', models.DateField(auto_now_add=True, verbose_name='采购日期')),
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
                ('test_id', models.PositiveIntegerField(help_text='A病人第X次挂号的第i项检验', verbose_name='检验序号')),
                ('issue_time', models.DateTimeField(auto_now_add=True, verbose_name='开具时间')),
                ('test_results', models.TextField(blank=True, max_length=400, null=True, verbose_name='检验结果')),
                ('payment_status', models.BooleanField(default=False, verbose_name='缴费状态')),
                ('inspect_status', models.BooleanField(default=False, help_text='还未开始检查（0）或正在检查及已完成检查（1）。', verbose_name='检查状态')),
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
                ('inspect_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='testitem_set', related_query_name='testitems', to='laboratory.testitemtype', verbose_name='检验项目类型')),
            ],
            options={
                'verbose_name': '检验项目',
                'verbose_name_plural': '检验项目',
            },
        ),
    ]
