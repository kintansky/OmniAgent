from django.db import models

# Create your models here.
class IpmanResource(models.Model):
    device_name = models.CharField(max_length=255)
    slot = models.CharField(max_length=4)
    slot_type = models.CharField(max_length=40)
    mda = models.CharField(max_length=4)
    mda_type = models.CharField(max_length=40)
    port = models.CharField(max_length=30)
    brand_width = models.CharField(max_length=20)
    port_status = models.CharField(max_length=10)
    port_phy_status = models.CharField(max_length=10)
    logic_port = models.CharField(max_length=20)
    logic_port_description = models.TextField()
    port_description = models.TextField()

    class Meta:
        unique_together = (('device_name', 'port'),)
