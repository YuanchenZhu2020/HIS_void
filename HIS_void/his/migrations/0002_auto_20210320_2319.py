# Generated by Django 3.1.7 on 2021-03-20 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('his', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': '部门表', 'verbose_name_plural': '部门表'},
        ),
        migrations.RenameField(
            model_name='loginlog',
            old_name='created_time',
            new_name='create_time',
        ),
    ]