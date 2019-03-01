from django.db import models

# Create your models here.
class PublicIpRecord(models.Model):
    device_ip = models.GenericIPAddressField(protocol='both', primary_key=True)
    device_name = models.CharField(max_length=255)
    logic_port = models.CharField(max_length=40)
    svlan = models.CharField(max_length=30)
    cvlan = models.CharField(max_length=30)
    ip_description = models.TextField(blank=True)
    record_time = models.DateTimeField()

    class Meta:
        ordering = ['-record_time', 'device_ip']
           
