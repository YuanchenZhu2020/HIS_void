# Generated by Django 3.1.7 on 2021-05-18 10:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import his.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rbac', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('dept', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rbac.usergroup', verbose_name='科室部门')),
                ('accept_patient', models.BooleanField(choices=[(0, '不接收患者'), (1, '接收患者')], default=0, help_text='是否向病人提供诊疗服务。', verbose_name='接收患者')),
                ('description', models.TextField(verbose_name='简介')),
            ],
            options={
                'verbose_name': '科室部门',
                'verbose_name_plural': '科室部门',
            },
            managers=[
                ('objects', his.models.DepartmentManager()),
            ],
        ),
        migrations.CreateModel(
            name='HospitalTitle',
            fields=[
                ('title_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='职称ID')),
                ('title_name', models.CharField(max_length=20, verbose_name='职称名称')),
            ],
            options={
                'verbose_name': '医院职称',
                'verbose_name_plural': '医院职称',
            },
            managers=[
                ('objects', his.models.HospitalTitleManager()),
            ],
        ),
        migrations.CreateModel(
            name='InpatientArea',
            fields=[
                ('area_id', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='病区')),
            ],
            options={
                'verbose_name': '病区',
                'verbose_name_plural': '病区',
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('job_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='工种编号')),
                ('job_name', models.CharField(max_length=20, verbose_name='工种名称')),
            ],
            options={
                'verbose_name': '工种',
                'verbose_name_plural': '工种',
            },
            managers=[
                ('objects', his.models.JobTypeManager()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='职工姓名')),
                ('gender', models.IntegerField(choices=[(0, '男'), (1, '女'), (2, '未知')], default=2, verbose_name='性别')),
                ('id_num', models.CharField(max_length=18, verbose_name='身份证号')),
                ('dept', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='his.department', verbose_name='科室部门')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='his.jobtype', verbose_name='工种')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='his.hospitaltitle', verbose_name='职称')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='登录信息')),
            ],
            options={
                'verbose_name': '职工',
                'verbose_name_plural': '职工',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='发送时间')),
                ('content', models.TextField(blank=True, null=True, verbose_name='通知正文')),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notice_set_send', related_query_name='notices_send', to='his.department', verbose_name='科室部门')),
                ('target_dept', models.ManyToManyField(related_name='notice_set_recv', related_query_name='notices_recv', to='his.Department', verbose_name='目标科室部门')),
            ],
            options={
                'verbose_name': '部门通知',
                'verbose_name_plural': '部门通知',
                'unique_together': {('dept', 'send_time')},
            },
        ),
        migrations.CreateModel(
            name='DutyRoster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('working_day', models.PositiveIntegerField(choices=[(1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五'), (6, '星期六'), (7, '星期日')], verbose_name='工作日')),
                ('duty_area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='duty_roster_set', related_query_name='duty_rosters', to='his.inpatientarea', verbose_name='负责病区')),
                ('medical_staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='duty_roster_set', related_query_name='duty_rosters', to='his.staff', verbose_name='医务人员')),
            ],
            options={
                'verbose_name': '医务人员排班表',
                'verbose_name_plural': '医务人员排班表',
                'unique_together': {('medical_staff', 'working_day')},
            },
        ),
        migrations.CreateModel(
            name='DeptAreaBed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bed_id', models.PositiveIntegerField(help_text='指定病区的第 n 个病床。', validators=[django.core.validators.MinValueValidator(1)], verbose_name='床位号')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='area_set', related_query_name='areas', to='his.inpatientarea', verbose_name='病区')),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dept_set', related_query_name='depts', to='his.department', verbose_name='科室')),
            ],
            options={
                'verbose_name': '科室-病区-床位',
                'verbose_name_plural': '科室-病区-床位',
                'unique_together': {('dept', 'area', 'bed_id')},
            },
        ),
    ]
