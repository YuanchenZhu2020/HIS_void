# Generated by Django 3.1.7 on 2021-06-05 11:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outpatient', '0006_titleregisternumber_registration_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titleregisternumber',
            name='registration_price',
            field=models.FloatField(blank=True, help_text='单位为￥', null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='挂号费用'),
        ),
    ]
