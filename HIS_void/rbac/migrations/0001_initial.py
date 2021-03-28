# Generated by Django 3.1.7 on 2021-03-20 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PermGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='权限组名称')),
            ],
            options={
                'verbose_name': '权限组',
                'verbose_name_plural': '权限组',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='权限名')),
                ('url', models.CharField(max_length=128, unique=True, verbose_name='URL')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('perm_code', models.CharField(max_length=32, verbose_name='权限代码')),
                ('perm_group', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.permgroup', verbose_name='所属权限组')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.permission', verbose_name='所属二级菜单')),
            ],
            options={
                'verbose_name': '权限表',
                'verbose_name_plural': '权限表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='角色名')),
                ('description', models.TextField(default='', max_length=300, verbose_name='角色描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('permissions', models.ManyToManyField(blank=True, to='rbac.Permission', verbose_name='拥有权限')),
            ],
            options={
                'verbose_name': '角色表',
                'verbose_name_plural': '角色表',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=6, verbose_name='登录账号')),
                ('password', models.CharField(max_length=256, verbose_name='登录密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('roles', models.ManyToManyField(to='rbac.Role', verbose_name='用户角色')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
            },
        ),
    ]