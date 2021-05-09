# Generated by Django 3.1.7 on 2021-05-09 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('his', '0003_notice'),
    ]

    operations = [
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
        ),
        migrations.AddField(
            model_name='staff',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='his.jobtype', verbose_name='工种'),
        ),
        migrations.AddField(
            model_name='staff',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='his.hospitaltitle', verbose_name='职称'),
        ),
    ]
