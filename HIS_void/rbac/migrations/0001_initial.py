# Generated by Django 3.1.7 on 2021-04-23 05:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import rbac.models


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
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
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
                'verbose_name': '权限',
                'verbose_name_plural': '权限',
            },
        ),
        migrations.CreateModel(
            name='PermissionsMixin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='超级用户具有全部权限', verbose_name='超级用户')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ug_id', models.IntegerField(help_text='用户组编号，取值范围为 1 ~ Inf', unique=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='用户组编号')),
                ('name', models.CharField(help_text='科室、部门或项目组名称', max_length=32, unique=True, verbose_name='用户组名称')),
            ],
            options={
                'verbose_name': '用户组',
                'verbose_name_plural': '用户组',
            },
            managers=[
                ('objects', rbac.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('permissionsmixin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rbac.permissionsmixin')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=6, unique=True, verbose_name='登录账号')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('is_active', models.BooleanField(default=True, help_text='决定该用户是否为活动账户', verbose_name='活动账户')),
                ('is_admin', models.BooleanField(default=False, help_text='决定该用户是否能够访问 /admin 页面', verbose_name='管理员')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
            bases=('rbac.permissionsmixin', models.Model),
        ),
        migrations.CreateModel(
            name='URLPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='URL访问权限的名称', max_length=255, unique=True, verbose_name='权限名')),
                ('url', models.CharField(help_text='用于匹配指定URL的正则表达式', max_length=128, unique=True, verbose_name='URL')),
                ('codename', models.CharField(help_text='简要概括URL访问权限作用的对象，建议使用英文单词和下划线', max_length=64, verbose_name='权限代码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('perm_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rbac.permgroup', verbose_name='所属权限组')),
            ],
            options={
                'verbose_name': 'URL访问权限',
                'verbose_name_plural': 'URL访问权限',
                'ordering': ['codename', 'url'],
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
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
            },
        ),
        migrations.AddField(
            model_name='permissionsmixin',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='用户所属的用户组，用户能够获取所属用户组的全部权限。', null=True, related_name='user_set', related_query_name='user', to='rbac.UserGroup', verbose_name='用户组'),
        ),
        migrations.AddField(
            model_name='permissionsmixin',
            name='url_permissions',
            field=models.ManyToManyField(blank=True, help_text='该用户具有的所有URL访问权限', related_name='urlperm_set', related_query_name='urlperm', to='rbac.URLPermission', verbose_name='URL访问权限'),
        ),
    ]
