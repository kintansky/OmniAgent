from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class IpmanResource(models.Model):
    device_name = models.CharField(max_length=255)
    slot = models.SmallIntegerField()
    slot_type = models.CharField(max_length=40)
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
            models.Index(fields=['logic_port']),
        ]


class IpRecord(models.Model):
    CHOICES = (
        ('private', 'Private'),
        ('public_outer', 'PublicOuter'),
        ('public_inner', 'PublicInner'),
    )
    device_ip = models.GenericIPAddressField(protocol='both')
    ip_mask = models.IntegerField(null=True)
    gateway = models.GenericIPAddressField(protocol='both', null=True)
    device_name = models.CharField(max_length=255)
    logic_port = models.CharField(max_length=40)
    logic_port_num = models.CharField(max_length=40, null=True)
    svlan = models.CharField(max_length=30)
    cvlan = models.CharField(max_length=30)
    ip_description = models.TextField(blank=True)
    ip_type = models.CharField(max_length=20, choices=CHOICES)
    record_time = models.DateTimeField()
    ip_func = models.CharField(max_length=40, null=True)

    class Meta:
        ordering = ['id', ]
        indexes = [
            models.Index(fields=['device_ip']),
            models.Index(fields=['logic_port_num']),
        ]


class PublicIpGateway(models.Model):
    gateway = models.GenericIPAddressField(protocol='both', primary_key=True)
    mask = models.SmallIntegerField()


class PublicIpSegment(models.Model):
    TYPE_CHOICES = (
        (-1, '私网'),
        (1, '公网外部使用'),
        (2, '公网内部使用'),
    )
    ip_segment = models.GenericIPAddressField(protocol='both')
    mask = models.IntegerField()
    segment_type = models.IntegerField(default=1, choices=TYPE_CHOICES)

    class Meta:
        unique_together = (('ip_segment', 'mask'),)
        ordering = ['id', ]


class ZxClientInfo(models.Model):
    group_id = models.BigIntegerField(null=True)
    client_name = models.CharField(max_length=255, null=True)
    product_id = models.BigIntegerField(null=True)
    device1 = models.CharField(max_length=255, null=True)
    device1_port = models.CharField(max_length=40, null=True)
    device2 = models.CharField(max_length=255, null=True)
    device2_port = models.CharField(max_length=40, null=True)
    gateway = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    ip = models.CharField(max_length=255, null=True)
    guard_level = models.CharField(max_length=20, null=True)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['ip']),
        ]


class IPAllocationBase(models.Model):
    # 基类
    order_num = models.CharField(max_length=255, null=True)
    client_name = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=5, null=True)
    ip = models.CharField(max_length=200, null=True)
    ip_mask = models.PositiveSmallIntegerField(null=True)
    gateway = models.GenericIPAddressField(protocol='both', null=True)
    bng = models.CharField(max_length=255, null=True)
    logic_port = models.CharField(max_length=20, null=True)
    svlan = models.PositiveIntegerField(default=0, null=True)
    cevlan = models.PositiveIntegerField(default=0, null=True)
    description = models.CharField(max_length=255, null=True)
    ip_func = models.CharField(max_length=4, null=True)
    olt = models.CharField(max_length=255, null=True)
    access_type = models.CharField(max_length=10, null=True)
    service_id = models.PositiveIntegerField(default=0)
    brand_width = models.PositiveIntegerField(default=0)
    group_id = models.PositiveIntegerField(default=0)
    product_id = models.PositiveIntegerField(default=0)
    network_type = models.CharField(max_length=5, null=True)
    community = models.CharField(max_length=50, null=True)
    rt = models.CharField(max_length=50, blank=True, null=True)
    rd = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        abstract = True


class IPAllocation(IPAllocationBase):
    comment = models.CharField(max_length=255, null=True)
    alc_user = models.CharField(max_length=10, null=True)
    alc_time = models.DateTimeField()
    last_mod_time = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-alc_time']
        indexes = [
            models.Index(fields=['ip']),
        ]


class IPMod(IPAllocationBase):
    mod_order_num = models.CharField(max_length=255, null=True)
    mod_msg = models.CharField(max_length=255, null=True)
    mod_user = models.CharField(max_length=10, null=True)
    mod_time = models.DateTimeField()
    mod_target_id = models.IntegerField()
    mod_type = models.CharField(max_length=5, null=True)

    class Meta:
        ordering = ['-mod_time']
        indexes = [
            models.Index(fields=['ip']),
            models.Index(fields=['client_name']),
            models.Index(fields=['product_id']),
        ]