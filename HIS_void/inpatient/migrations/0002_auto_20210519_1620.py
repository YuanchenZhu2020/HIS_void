# Generated by Django 3.1.7 on 2021-05-19 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0001_initial'),
        ('inpatient', '0001_initial'),
        ('pharmacy', '0001_initial'),
        ('his', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nursingrecord',
            name='medical_staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nursing_record_set', related_query_name='nursing_records', to='his.staff', verbose_name='责任护士'),
        ),
        migrations.AddField(
            model_name='nursingrecord',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nursing_record_set', related_query_name='nursing_records', to='patient.patientuser', verbose_name='患者'),
        ),
        migrations.AddField(
            model_name='hospitalregistration',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='his.inpatientarea', verbose_name='所属病区'),
        ),
        migrations.AddField(
            model_name='hospitalregistration',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='his.department', verbose_name='所属科室'),
        ),
        migrations.AlterUniqueTogether(
            name='operationinfo',
            unique_together={('registration_info', 'operation_id')},
        ),
        migrations.AlterUniqueTogether(
            name='nursingrecord',
            unique_together={('medical_staff', 'patient', 'nursing_date')},
        ),
        migrations.AddField(
            model_name='narcoticinfo',
            name='medical_staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='narcotic_set', related_query_name='narcotics', to='his.staff', verbose_name='麻醉师'),
        ),
        migrations.AddField(
            model_name='narcoticinfo',
            name='medicine_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='narcotic_set', related_query_name='narcotics', to='pharmacy.medicineinfo', verbose_name='麻醉药品信息'),
        ),
    ]
