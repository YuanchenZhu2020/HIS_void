# Generated by Django 3.1.7 on 2021-06-05 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('outpatient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalRegistration',
            fields=[
                ('registration_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='outpatient.registrationinfo', verbose_name='挂号信息')),
                ('bed_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='床位号')),
                ('reg_date', models.DateField(blank=True, null=True, verbose_name='入院日期')),
                ('care_level', models.PositiveIntegerField(choices=[(1, '一级护理'), (2, '二级护理'), (3, '三级护理'), (4, '四级护理')], default=3, verbose_name='护理级别')),
                ('duration', models.PositiveIntegerField(blank=True, null=True, verbose_name='住院天数')),
                ('kin_phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='家属电话')),
                ('discharge_status', models.PositiveIntegerField(choices=[(0, '未出院'), (1, '即将出院'), (2, '已出院')], default=0, verbose_name='出院状态')),
                ('payment_status', models.BooleanField(default=False, verbose_name='缴费状态')),
            ],
            options={
                'verbose_name': '入院登记信息',
                'verbose_name_plural': '入院登记信息',
            },
        ),
        migrations.CreateModel(
            name='NursingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nursing_date', models.DateField(auto_now_add=True, verbose_name='护理时间')),
                ('systolic', models.PositiveIntegerField(blank=True, null=True, verbose_name='收缩压')),
                ('diastolic', models.PositiveIntegerField(blank=True, null=True, verbose_name='舒张压')),
                ('temperature', models.FloatField(blank=True, null=True, verbose_name='体温')),
                ('note', models.TextField(blank=True, max_length=200, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '护理记录',
                'verbose_name_plural': '护理记录',
            },
        ),
        migrations.CreateModel(
            name='OperationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_id', models.PositiveIntegerField(help_text='局部编号：每个医生-患者之间进行的第几场手术', verbose_name='手术编号')),
                ('operation_level', models.PositiveIntegerField(choices=[(1, '一级手术'), (2, '二级手术'), (3, '三级手术'), (4, '四级手术')], default=1, verbose_name='手术等级')),
                ('operation_date', models.DateField(verbose_name='手术日期')),
                ('operation_name', models.CharField(max_length=40, verbose_name='手术名称')),
                ('operation_result', models.CharField(blank=True, max_length=20, null=True, verbose_name='手术结果')),
                ('operation_duration', models.PositiveBigIntegerField(blank=True, help_text='以分钟为单位的手术持续时间。', null=True, verbose_name='手术持续时间')),
                ('operation_recover', models.CharField(blank=True, max_length=10, null=True, verbose_name='预后结果')),
                ('payment_status', models.BooleanField(default=False, verbose_name='缴费状态')),
                ('registration_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operation_set', related_query_name='operations', to='outpatient.registrationinfo', verbose_name='挂号信息')),
            ],
            options={
                'verbose_name': '手术信息',
                'verbose_name_plural': '手术信息',
            },
        ),
        migrations.CreateModel(
            name='NarcoticInfo',
            fields=[
                ('operation_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='narcotic_set', related_query_name='narcotics', serialize=False, to='inpatient.operationinfo', verbose_name='手术信息')),
            ],
            options={
                'verbose_name': '麻醉信息',
                'verbose_name_plural': '麻醉信息',
            },
        ),
    ]
