# Generated by Django 3.1.7 on 2021-06-05 11:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outpatient', '0005_remove_registrationinfo_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='titleregisternumber',
            name='registration_price',
            field=models.FloatField(default=0, help_text='单位为￥', validators=[django.core.validators.MinValueValidator(1)], verbose_name='挂号费用'),
            preserve_default=False,
        ),
    ]
