from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class OpticalMoudleDiff(models.Model):
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    now_moudle = models.CharField(max_length=60)
    ever_moudle = models.CharField(max_length=60)
    STATUS_CHOICES = (
        ('NEW', 'plugin'),
        ('MISS', 'missing'),
        ('CH', 'changed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    record_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-record_time']


class PortErrorDiff(models.Model):
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    nowCRC = models.IntegerField()
    nowIpv4HeaderError = models.IntegerField()
    everCRC = models.IntegerField()
    everIpv4HeaderError = models.IntegerField()
    stateCRC = models.FloatField()  # CRC状态，1为正常，0为异常
    stateIpv4HeadError = models.FloatField()    # head状态，1为正常，0为异常
    # record_time = models.DateTimeField(auto_now_add=True)
    record_time = models.DateTimeField()

    class Meta:
        # app_label = 'networkresource'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['device_name']),
        ]


class PortErrorFixRecord(models.Model):
    target = models.ForeignKey(PortErrorDiff, on_delete=models.DO_NOTHING)
    problem_type = models.CharField(max_length=40)
    problem_detail = models.TextField()
    begin_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    worker = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class PortPerf(models.Model):
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    # 发光字段
    tx_now_power = models.FloatField()
    tx_high_warm = models.FloatField()
    tx_low_warm = models.FloatField()
    tx_state = models.IntegerField()
    # 收光字段
    rx_now_power = models.FloatField()
    rx_high_warm = models.FloatField()
    rx_low_warm = models.FloatField()
    rx_state = models.IntegerField()
    # 利用率字段
    utility_in = models.FloatField()
    utility_out = models.FloatField()
    record_time = models.DateTimeField()

    class Meta:
        app_label = 'networkresource'
        ordering = ['-record_time']
        indexes = [
            models.Index(fields=['device_name']),
            models.Index(fields=['port']),
        ]


class OneWayDevice(models.Model):
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    port_status = models.CharField(max_length=10)
    port_phy_status = models.CharField(max_length=10)
    port_des = models.CharField(max_length=255)
    record_time = models.DateTimeField()

    class Meta:
        ordering = ['-record_time']
        indexes = [
            models.Index(fields=['device_name']),
            models.Index(fields=['port']),
        ]
