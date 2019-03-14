from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class IpmanResource(models.Model):
    device_name = models.CharField(max_length=255)
    # slot = models.CharField(max_length=4)
    slot = models.SmallIntegerField()
    slot_type = models.CharField(max_length=40)
    # mda = models.CharField(max_length=4)
    mda = models.SmallIntegerField()
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
        indexes = [
            models.Index(fields=['slot']),
            models.Index(fields=['mda']),
        ]

class IpRecord(models.Model):
    device_ip = models.GenericIPAddressField(protocol='both')
    device_name = models.CharField(max_length=255)
    logic_port = models.CharField(max_length=40)
    svlan = models.CharField(max_length=30)
    cvlan = models.CharField(max_length=30)
    ip_description = models.TextField(blank=True)
    record_time = models.DateTimeField()

    class Meta:
        ordering = ['id',]

class PublicIpAllocation(models.Model):
    ies = models.CharField(max_length=20, blank=True, null=True)   # 看是否能改成int
    order_num = models.CharField(max_length=255, blank=True, null=True)
    client_num = models.CharField(max_length=100)
    product_num = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(protocol='both')
    mask = models.SmallIntegerField()
    gateway = models.CharField(max_length=100)
    link_tag = models.SmallIntegerField()
    device_name = models.CharField(max_length=255)
    logic_port = models.CharField(max_length=40)
    svlan = models.CharField(max_length=30)
    cvlan = models.CharField(max_length=30)
    access_type = models.CharField(max_length=10, blank=True, null=True)
    olt_name = models.CharField(max_length=255, blank=True, null=True)
    client_name = models.CharField(max_length=255)
    ip_description = models.TextField(blank=True, null=True)
    up_brandwidth = models.SmallIntegerField(blank=True, null=True)
    down_brandwidth = models.SmallIntegerField()
    alc_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='plcip_alc_user')
    alc_time = models.DateTimeField(auto_now_add=True)
    # ip调整操作
    adj_order = models.CharField(max_length=255, blank=True, null=True)
    adj_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='plcip_adj_user')
    adj_time = models.DateTimeField(blank=True, null=True)
    # ip销户操作
    close_order = models.CharField(max_length=255, blank=True, null=True)
    close_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='plcip_close_user')
    close_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'watchdog'  # 因为cmdb没有auth_user表格，只能在omni_agent主数据库里面建表，否则无法关联fk
        ordering = ['alc_time',]

class PrivateIpAllocation(models.Model):
    service = models.CharField(max_length=50, blank=True, null=True)
    community = models.CharField(max_length=50, blank=True, null=True)   # 看是否能改成int
    service_id = models.CharField(max_length=50, blank=True, null=True)
    rd = models.CharField(max_length=50, blank=True, null=True)
    rt = models.CharField(max_length=50, blank=True, null=True)
    order_num = models.CharField(max_length=255, blank=True, null=True)
    client_name = models.CharField(max_length=255)
    client_num = models.CharField(max_length=100)
    product_num = models.CharField(max_length=100)
    device_name = models.CharField(max_length=255)
    logic_port = models.CharField(max_length=40)
    svlan = models.CharField(max_length=30)
    cvlan = models.CharField(max_length=30)
    olt_name = models.CharField(max_length=255, blank=True, null=True)
    access_type = models.CharField(max_length=10, blank=True, null=True)
    ip = models.GenericIPAddressField(protocol='both')
    gateway = models.GenericIPAddressField(protocol='both', null=True)   # 10.0.64.1
    ipsegment = models.CharField(max_length=100, null=True)    # 10.0.64.0/24
    ip_description = models.TextField(blank=True, null=True)
    alc_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='prvip_alc_user')
    alc_time = models.DateTimeField(auto_now_add=True)
    # ip调整操作
    adj_order = models.CharField(max_length=255, blank=True, null=True)
    adj_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='prvip_adj_user')
    adj_time = models.DateTimeField(blank=True, null=True)
    # ip销户操作
    close_order = models.CharField(max_length=255, blank=True, null=True)
    close_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='prvip_close_user')
    close_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'watchdog'  # 因为cmdb没有auth_user表格，只能在omni_agent主数据库里面建表，否则无法关联fk
        ordering = ['alc_time',]