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
    stateCRC = models.CharField(max_length=20, choices=STATE_CHOICES)
    stateIpv4HeadError = models.CharField(max_length=20, choices=STATE_CHOICES)
    record_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-record_time']