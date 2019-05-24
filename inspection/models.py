from django.db import models

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
    port = models.CharField(max_length=30)
    nowCRC = models.IntegerField()
    nowIpv4HeaderError = models.IntegerField()
    everCRC = models.IntegerField()
    everIpv4HeaderError = models.IntegerField()
    STATE_CHOICES = (
        ('increase', 'INCREASING'),
        ('fair', 'fair'),
    )
    stateCRC = models.FloatField()
    stateIpv4HeadError = models.FloatField()
    # stateCRC = models.CharField(max_length=20, choices=STATE_CHOICES)
    # stateIpv4HeadError = models.CharField(max_length=20, choices=STATE_CHOICES)
    record_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'networkresource'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['device_name']),
        ]

class PortPerf(models.Model):
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=30)

    tx_now_power = models.FloatField()
    tx_high_warm = models.FloatField()
    tx_low_warm = models.FloatField()
    tx_state = models.IntegerField()

    rx_now_power = models.FloatField()
    rx_high_warm = models.FloatField()
    rx_low_warm = models.FloatField()
    rx_state = models.IntegerField()
    
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
