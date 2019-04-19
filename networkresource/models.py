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
    CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
    )
    device_ip = models.GenericIPAddressField(protocol='both')
    ip_mask = models.IntegerField(null=True)
    device_name = models.CharField(max_length=255)
    logic_port = models.CharField(max_length=40)
    svlan = models.CharField(max_length=30)
    cvlan = models.CharField(max_length=30)
    ip_description = models.TextField(blank=True)
    ip_type = models.CharField(max_length=10, choices=CHOICES)
    record_time = models.DateTimeField()

    class Meta:
        ordering = ['id',]

class PublicIpGateway(models.Model):
    gateway = models.GenericIPAddressField(protocol='both', primary_key=True)
    mask = models.SmallIntegerField()

    class Meta:
        app_label = 'watchdog'

class PublicIpSegment(models.Model):
    TYPE_CHOICES = (
        (1, '公网外部使用'),
        (2, '公网内部使用'),
        (3, '私网')
    )
    ip_segment = models.GenericIPAddressField(protocol='both')
    mask = models.IntegerField()
    segment_type = models.IntegerField(default=1, choices=TYPE_CHOICES)

    class Meta:
        unique_together = (('ip_segment', 'mask'),)
        ordering = ['id',]
        app_label = 'watchdog'

class PublicIpAllocation(models.Model):
    ies = models.CharField(max_length=20, blank=True, null=True)   # 看是否能改成int
    order_num = models.CharField(max_length=255, blank=True, null=True)
    client_num = models.CharField(max_length=100)
    product_num = models.CharField(max_length=100)
    ip = models.GenericIPAddressField(protocol='both')
    mask = models.SmallIntegerField()
    gateway = models.CharField(max_length=100)
    link_tag = models.SmallIntegerField(blank=True, null=True)
    device_name = models.CharField(max_length=255)
    logic_port = models.CharField(max_length=40)
    svlan = models.CharField(max_length=30)
    cvlan = models.CharField(max_length=30, blank=True, null=True)
    access_type = models.CharField(max_length=10, blank=True, null=True)
    olt_name = models.CharField(max_length=255, blank=True, null=True)
    client_name = models.CharField(max_length=255)
    ip_description = models.TextField(blank=True, null=True)
    up_brandwidth = models.SmallIntegerField(blank=True, null=True)
    down_brandwidth = models.SmallIntegerField()
    alc_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='plcip_alc_user')
    alc_time = models.DateTimeField(auto_now_add=True)    # 外部数据导入时注释
    # alc_time = models.DateTimeField()   # 外部数据导入时使用
    # 取消该模型内的调整记录，增加状态标记：在用、销户
    state = models.CharField(max_length=10)

    class Meta:
        app_label = 'watchdog'  # 因为cmdb没有auth_user表格，只能在omni_agent主数据库里面建表，否则无法关联fk
        ordering = ['-alc_time',]

class PublicIpModRecord(models.Model):
    mod_target = models.ForeignKey(PublicIpAllocation, on_delete=models.DO_NOTHING)
    mod_order = models.CharField(max_length=255)
    mod_msg = models.TextField()
    mod_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='plcip_mod_user')
    # record_time = models.DateTimeField()
    record_time = models.DateTimeField(auto_now_add=True)

    # 本次修改前的分配信息，用于记录备份
    ever_ies = models.CharField(max_length=20, blank=True, null=True)   # 看是否能改成int
    ever_client_num = models.CharField(max_length=100, null=True)
    ever_product_num = models.CharField(max_length=100, null=True)
    ever_ip = models.GenericIPAddressField(protocol='both', null=True)
    ever_mask = models.SmallIntegerField(null=True)
    ever_gateway = models.CharField(max_length=100, null=True)
    ever_link_tag = models.SmallIntegerField(blank=True, null=True)
    ever_device_name = models.CharField(max_length=255, null=True)
    ever_logic_port = models.CharField(max_length=40, null=True)
    ever_svlan = models.CharField(max_length=30, null=True)
    ever_cvlan = models.CharField(max_length=30, blank=True, null=True)
    ever_access_type = models.CharField(max_length=10, blank=True, null=True)
    ever_olt_name = models.CharField(max_length=255, blank=True, null=True)
    ever_client_name = models.CharField(max_length=255, null=True)
    ever_ip_description = models.TextField(blank=True, null=True)
    ever_up_brandwidth = models.SmallIntegerField(blank=True, null=True)
    ever_down_brandwidth = models.SmallIntegerField(null=True)
    ever_state = models.CharField(max_length=10, null=True)

    class Meta:
        app_label = 'watchdog'  # 因为cmdb没有auth_user表格，只能在omni_agent主数据库里面建表，否则无法关联fk
        ordering = ['-record_time',]
    
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
    alc_time = models.DateTimeField(auto_now_add=True)    # 外部数据导入时注释
    # alc_time = models.DateTimeField()   # 外部数据导入时使用
    state = models.CharField(max_length=10)

    class Meta:
        app_label = 'watchdog'  # 因为cmdb没有auth_user表格，只能在omni_agent主数据库里面建表，否则无法关联fk
        ordering = ['-alc_time',]

class PrivateIpModRecord(models.Model):
    mod_target = models.ForeignKey(PrivateIpAllocation, on_delete=models.DO_NOTHING)
    mod_order = models.CharField(max_length=255)
    mod_msg = models.TextField()
    mod_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='prvip_mod_user')
    # record_time = models.DateTimeField()
    record_time = models.DateTimeField(auto_now_add=True)
    # 本次修改前的分配信息，用于记录备份
    ever_service = models.CharField(max_length=50, blank=True, null=True)
    ever_community = models.CharField(max_length=50, blank=True, null=True)   # 看是否能改成int
    ever_service_id = models.CharField(max_length=50, blank=True, null=True)
    ever_rd = models.CharField(max_length=50, blank=True, null=True)
    ever_rt = models.CharField(max_length=50, blank=True, null=True)
    ever_client_name = models.CharField(max_length=255, null=True)
    ever_client_num = models.CharField(max_length=100, null=True)
    ever_product_num = models.CharField(max_length=100, null=True)
    ever_device_name = models.CharField(max_length=255, null=True)
    ever_logic_port = models.CharField(max_length=40, null=True)
    ever_svlan = models.CharField(max_length=30, null=True)
    ever_cvlan = models.CharField(max_length=30, null=True)
    ever_olt_name = models.CharField(max_length=255, blank=True, null=True)
    ever_access_type = models.CharField(max_length=10, blank=True, null=True)
    ever_ip = models.GenericIPAddressField(protocol='both', null=True)
    ever_gateway = models.GenericIPAddressField(protocol='both', null=True)   # 10.0.64.1
    ever_ipsegment = models.CharField(max_length=100, null=True)    # 10.0.64.0/24
    ever_ip_description = models.TextField(blank=True, null=True)
    ever_state = models.CharField(max_length=10, null=True)

    class Meta:
        app_label = 'watchdog'  # 因为cmdb没有auth_user表格，只能在omni_agent主数据库里面建表，否则无法关联fk
        ordering = ['-record_time',]