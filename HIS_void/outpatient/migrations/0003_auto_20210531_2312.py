# Generated by Django 3.1.7 on 2021-05-31 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
        ('his', '0001_initial'),
        ('outpatient', '0002_auto_20210529_2305'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='registrationinfo',
            unique_together={('patient', 'reg_id'), ('patient', 'medical_staff', 'registration_date')},
        ),
    ]