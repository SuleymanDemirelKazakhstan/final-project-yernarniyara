from django.db import models
from django.db.models import JSONField


# Create your models here.

class Users(models.Model):
    user_data = JSONField(verbose_name='user_data', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="create_time")


class MedicalInstitutions(models.Model):
    medic_data = JSONField(verbose_name='medic_data', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="create_time")


class MedicalUsers(models.Model):
    medical_user_data = JSONField(verbose_name='medical_user_data', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="create_time")


class WaitingMedicalUsers(models.Model):
    waiting_medic_data = JSONField(verbose_name='waiting_medi_data', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="create_time")


class AllBonuses(models.Model):
    bonus_name = models.CharField(max_length=100, verbose_name='bonus_name', default='')
    bonus_data = JSONField(verbose_name='bonus_data', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="create_time")


class BloodSavings(models.Model):
    blood_data = JSONField(verbose_name='user_data', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="create_time")
