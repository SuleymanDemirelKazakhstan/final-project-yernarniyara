# Generated by Django 3.1.6 on 2021-02-24 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllBonuses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus_name', models.CharField(default='', max_length=100, verbose_name='bonus_name')),
                ('bonus_data', models.JSONField(default=dict, verbose_name='bonus_data')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
            ],
        ),
        migrations.CreateModel(
            name='BloodSavings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_data', models.JSONField(default=dict, verbose_name='user_data')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalInstitutions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medic_data', models.JSONField(default=dict, verbose_name='medic_data')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_user_data', models.JSONField(default=dict, verbose_name='medical_user_data')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_data', models.JSONField(default=dict, verbose_name='user_data')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
            ],
        ),
        migrations.CreateModel(
            name='WaitingMedicalUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waiting_medic_data', models.JSONField(default=dict, verbose_name='waiting_medi_data')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
            ],
        ),
    ]
