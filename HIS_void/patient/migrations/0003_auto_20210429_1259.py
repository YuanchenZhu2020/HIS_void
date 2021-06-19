# Generated by Django 3.1.7 on 2021-04-29 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_patientuser_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientuser',
            name='is_admin',
            field=models.BooleanField(default=False, editable=False, help_text='决定该用户是否能够访问 /admin 页面。', verbose_name='管理员'),
        ),
        migrations.AlterField(
            model_name='patientuser',
            name='phone',
            field=models.CharField(max_length=11, null=True, verbose_name='手机号码'),
        ),
    ]