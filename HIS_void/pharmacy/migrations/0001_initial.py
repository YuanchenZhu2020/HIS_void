# Generated by Django 3.1.7 on 2021-06-13 14:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MedicineInfo',
            fields=[
                ('medicine_id', models.CharField(help_text='药品的全局编号', max_length=6, primary_key=True, serialize=False, unique=True, verbose_name='药品编号')),
                ('medicine_name', models.CharField(max_length=100, verbose_name='药品名称')),
                ('content_spec', models.CharField(max_length=20, verbose_name='含量规格')),
                ('package_spec', models.CharField(max_length=20, verbose_name='包装规格')),
                ('cost_price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='成本价')),
                ('retail_price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='零售价')),
                ('stock_num', models.PositiveIntegerField(default=0, verbose_name='库存数量')),
                ('shelf_day', models.PositiveIntegerField(help_text='以天为单位的保质期。', verbose_name='保质期')),
                ('special', models.IntegerField(choices=[(1, '麻醉药品'), (2, '精神药品'), (3, '毒性药品'), (4, '放射性药品'), (0, '普通药品')], default=0, verbose_name='特殊药品')),
                ('OTC', models.BooleanField(default=False, verbose_name='是否处方药')),
            ],
            options={
                'verbose_name': '药品信息',
                'verbose_name_plural': '药品信息',
            },
        ),
        migrations.CreateModel(
            name='MedicinePurchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_num', models.PositiveIntegerField(verbose_name='批次编号')),
                ('purchase_date', models.DateField(verbose_name='采购日期')),
                ('purchase_quantity', models.PositiveIntegerField(verbose_name='采购数量')),
                ('medicine_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicine_purchase_set', related_query_name='medicine_purchases', to='pharmacy.medicineinfo', verbose_name='药品信息')),
            ],
            options={
                'verbose_name': '药品采购记录',
                'verbose_name_plural': '药品采购记录',
                'unique_together': {('medicine_info', 'batch_num')},
            },
        ),
    ]
