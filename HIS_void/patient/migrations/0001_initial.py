# Generated by Django 3.1.7 on 2021-05-19 08:20

from django.db import migrations, models
import django.db.models.deletion
import patient.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientURLPermission',
            fields=[
                ('urlpermission_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='rbac.urlpermission')),
            ],
            options={
                'verbose_name': '患者URL访问权限',
                'verbose_name_plural': '患者URL访问权限',
                'ordering': ['codename', 'url'],
            },
            bases=('rbac.urlpermission',),
        ),
        migrations.CreateModel(
            name='PatientUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('patient_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='就诊号')),
                ('id_type', models.IntegerField(choices=[(0, '中国大陆身份证'), (1, '港澳居民来往内地通行证'), (2, '台湾居民来往大陆通行证'), (3, '护照')], default=0, verbose_name='证件类型')),
                ('id_number', models.CharField(max_length=18, validators=[patient.validators.IDNumberValidator()], verbose_name='证件号')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('gender', models.IntegerField(choices=[(0, '男'), (1, '女')], default=0, verbose_name='性别')),
                ('birthday', models.DateField(verbose_name='出生日期')),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='手机号码')),
                ('past_illness', models.TextField(verbose_name='既往史')),
                ('allegic_history', models.TextField(verbose_name='过敏史')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('is_admin', models.BooleanField(default=False, editable=False, help_text='决定该用户是否能够访问 /admin 页面。', verbose_name='管理员')),
            ],
            options={
                'verbose_name': '患者',
                'verbose_name_plural': '患者',
            },
        ),
    ]
