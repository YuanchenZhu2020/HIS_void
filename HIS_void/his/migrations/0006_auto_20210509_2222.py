# Generated by Django 3.1.7 on 2021-05-09 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('his', '0005_dutyroster'),
    ]

    operations = [
        migrations.CreateModel(
            name='InpatientArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_id', models.CharField(max_length=2, unique=True, verbose_name='病区')),
            ],
            options={
                'verbose_name': '病区',
                'verbose_name_plural': '病区',
            },
        ),
        migrations.AlterField(
            model_name='dutyroster',
            name='duty_area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='duty_roster_set', related_query_name='duty_rosters', to='his.inpatientarea', verbose_name='负责病区'),
        ),
    ]
