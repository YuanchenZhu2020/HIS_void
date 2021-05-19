# Generated by Django 3.1.7 on 2021-05-17 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription_date', models.DateTimeField(auto_created=True, editable=False, verbose_name='开具时间')),
                ('medicine_num', models.PositiveIntegerField(blank=True, verbose_name='药品种类数')),
                ('medical_advice', models.TextField(blank=True, max_length=400, null=True, verbose_name='医嘱')),
                ('payment_status', models.BooleanField(default=False, verbose_name='缴费状态')),
            ],
            options={
                'verbose_name': '患者处方',
                'verbose_name_plural': '患者处方',
            },
        ),
        migrations.CreateModel(
            name='PrescriptionDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail_id', models.PositiveIntegerField(verbose_name='细节编号')),
                ('medicine_quantity', models.PositiveIntegerField(verbose_name='药品数量')),
            ],
            options={
                'verbose_name': '处方细节',
                'verbose_name_plural': '处方细节',
            },
        ),
        migrations.CreateModel(
            name='RegistrationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField(auto_created=True, editable=False, help_text='通过网页预约挂号的时间', verbose_name='预约时间')),
                ('reg_id', models.PositiveIntegerField(help_text='该患者此生挂的第n个号', verbose_name='患者挂号编号')),
                ('registration_date', models.DateTimeField(help_text='预约就诊的时间', verbose_name='挂号时间')),
                ('reg_class', models.IntegerField(choices=[(0, '门诊'), (1, '急诊')], default=0, verbose_name='就诊类别')),
                ('illness_date', models.DateField(blank=True, verbose_name='患病日期')),
                ('chief_complaint', models.TextField(blank=True, max_length=512, verbose_name='患者主诉')),
                ('diagnosis_results', models.TextField(blank=True, max_length=512, verbose_name='确诊结果')),
            ],
            options={
                'verbose_name': '挂号信息',
                'verbose_name_plural': '挂号信息',
            },
        ),
        migrations.CreateModel(
            name='RemainingRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_date', models.DateField(verbose_name='挂号日期')),
                ('remain_quantity', models.PositiveIntegerField(verbose_name='当日剩余挂号数')),
            ],
            options={
                'verbose_name': '医生剩余挂号数',
                'verbose_name_plural': '医生剩余挂号数',
            },
        ),
    ]
