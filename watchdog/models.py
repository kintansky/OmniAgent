from django.db import models

# Create your models here.
class DeviceManufactor(models.Model):
    manufactor_name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.manufactor_name
    
class Device(models.Model):
    device_name = models.CharField(max_length=255, primary_key=True)
    device_ip = models.GenericIPAddressField(protocol='both')
    device_manufactor = models.ForeignKey(DeviceManufactor, on_delete=models.DO_NOTHING)
    device_network = models.CharField(max_length=100)
    login_port = models.SmallIntegerField()
    login_user = models.CharField(max_length=30)
    login_password = models.CharField(max_length=30)

    class Meta:
        ordering = ['device_ip']

class CommandLine(models.Model):
    cmd_manufactor = models.ForeignKey(DeviceManufactor, on_delete=models.DO_NOTHING)
    FUNC_CHOICES = (
        ('BK', 'backup'),
        ('XM1_0', 'exam_home_user_amount'),
        ('XM1_1', 'exam_otv_user_amount'),
        ('XM1_2', 'exam_ims_amount'),
        ('XM1_3', 'exam_itms_amount'),
        ('XM2_0', 'exam_cpu_perf'),
        ('XM2_1', 'exam_memory_perf'),
        ('XM2_2', 'exam_home_user_ippool'),
        ('SH', 'show'),
        ('OTH', 'others')
        )
    cmd_func = models.CharField(max_length=20, choices=FUNC_CHOICES)
    cmd_content = models.TextField()
    cmd_description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['id']
