# Generated by Django 3.1.7 on 2021-04-23 05:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_id', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)], verbose_name='科室部门编号')),
                ('name', models.CharField(max_length=32, verbose_name='科室部门名称')),
            ],
            options={
                'verbose_name': '科室部门',
                'verbose_name_plural': '科室部门',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='职工姓名')),
                ('gender', models.IntegerField(choices=[(0, '男'), (1, '女')], verbose_name='性别')),
                ('id_num', models.CharField(max_length=18, verbose_name='身份证号')),
                ('dept', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='his.department', verbose_name='科室部门')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='登录信息')),
            ],
            options={
                'verbose_name': '职工',
                'verbose_name_plural': '职工',
            },
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField(auto_now_add=True, verbose_name='登录时间')),
                ('ip_address', models.CharField(max_length=256, verbose_name='登录IP')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='his.staff', verbose_name='职工')),
            ],
            options={
                'verbose_name': '登录日志',
                'verbose_name_plural': '登录日志',
            },
        ),
    ]
