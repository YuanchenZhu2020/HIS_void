# Generated by Django 3.1.7 on 2021-04-29 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_auto_20210429_1300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientuser',
            old_name='birthday',
            new_name='birth',
        ),
    ]
