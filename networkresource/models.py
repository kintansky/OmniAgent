from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class OpticalMoudle(models.Model):
    device = models.CharField(max_length=255)
    port = models.CharField(max_length=30)
    moudle = models.CharField(max_length=60)
    record_time = models.DateTimeField()

    class Meta:
        db_table = 'MR_REC_optical_moudle_record'
        indexes = [
            models.Index(fields=['device']),
            models.Index(fields=['port']),
        ]

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
        db_table = 'MR_REC_ipman_resource'
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
        db_table = 'MR_REC_ip_record'
        ordering = ['id', ]
        indexes = [
            models.Index(fields=['device_ip']),
            models.Index(fields=['logic_port_num']),
            models.Index(fields=['device_name']),
        ]


# class PublicIpGateway(models.Model):
#     gateway = models.GenericIPAddressField(protocol='both')
#     olt_cnt = models.PositiveIntegerField(default=0)
#     olts = models.CharField(max_length=255, null=True)
#     # mask = models.SmallIntegerField()

#     class Meta:
#         # db_table = 'MR_REC_public_ip_gateway'
#         db_table = 'MR_STS_public_gateway'


class PublicIpSegment(models.Model):
    upper_segment = models.GenericIPAddressField(protocol='both')
    upper_mask = models.PositiveSmallIntegerField()
    specialization = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'MR_REC_public_segment_reference'
        unique_together = (('upper_segment', 'upper_mask'),)
        ordering = ['id', ]


class PublicIPSegmentSchema(models.Model):
    ip = models.GenericIPAddressField(protocol='both', unique=True)
    upper_segment = models.GenericIPAddressField(protocol='both')
    upper_mask = models.PositiveSmallIntegerField()
    state = models.SmallIntegerField(default=0) # 默认0，预占-1，正常启用1，下沉地址2
    subnet_gateway = models.CharField(max_length=10, null=True)
    subnet_mask = models.PositiveSmallIntegerField(null=True)
    access_bng = models.CharField(max_length=255, null=True)    # 这里记录的是两台bng，以/分割
    access_olt = models.CharField(max_length=255, null=True)    # 记录可能是多台olt，以/分割
    access_type = models.CharField(max_length=10, null=True)  # 前端使用choice限制 
    alc_user = models.CharField(max_length=10, null=True)
    alc_time = models.DateTimeField()

    class Meta:
        db_table = 'MR_REC_public_segment_schema'


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
        db_table = 'MR_REC_group_client_info'
        ordering = ['id']
        indexes = [
            models.Index(fields=['ip']),
        ]

class ICP(models.Model):
    identify_id = models.CharField(max_length=100)  # 必填
    guard_level = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=10, null=True)
    district = models.CharField(max_length=10, null=True)
    distributor = models.CharField(max_length=10, null=True)
    distributor_contact = models.CharField(max_length=20, null=True)
    demand = models.TextField(null=True)
    bandwidth_up = models.PositiveIntegerField(default=0)
    bandwidth_dwn = models.PositiveIntegerField(default=0)
    client_tech = models.CharField(max_length=10, null=True)
    client_tech_contact = models.CharField(max_length=20, null=True)
    demand_ipv4_amount = models.PositiveIntegerField(default=0)
    demand_ipv6_amount = models.PositiveIntegerField(default=0)
    client_address = models.CharField(max_length=255, null=True)
    businessman = models.CharField(max_length=10, null=True)
    businessman_contact = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'MR_REC_icp_info'
        ordering = ['id',]
        # indexes = [
        #     models.Index(fields=['identify_id']),
        # ]

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
    group_id = models.BigIntegerField(default=0)
    product_id = models.BigIntegerField(default=0)
    network_type = models.CharField(max_length=5, null=True)
    community = models.CharField(max_length=50, null=True)
    rt = models.CharField(max_length=50, blank=True, null=True)
    rd = models.CharField(max_length=50, blank=True, null=True)
    icp = models.ForeignKey(
        ICP,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class IPAllocation(IPAllocationBase):
    comment = models.CharField(max_length=255, null=True)
    alc_user = models.CharField(max_length=10, null=True)
    alc_time = models.DateTimeField()
    last_mod_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'MR_REC_ip_allocation'
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
        db_table = 'MR_REC_ip_mod_record'
        ordering = ['-mod_time']
        indexes = [
            models.Index(fields=['ip']),
            models.Index(fields=['client_name']),
            models.Index(fields=['product_id']),
        ]
        

class OltBngRef(models.Model):
    bng = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    logic_port = models.CharField(max_length=40)
    description = models.CharField(max_length=255)
    olt_num = models.CharField(max_length=10)
    district = models.CharField(max_length=10)
    olt = models.CharField(max_length=255)
    olt_state = models.CharField(max_length=20, null=True)
    olt_type = models.CharField(max_length=10, null=True)
    olt_ip = models.GenericIPAddressField()

    class Meta:
        db_table = 'MR_REP_olt_bng_references'
        indexes = [
            models.Index(fields=['bng']),
            models.Index(fields=['logic_port']),
            models.Index(fields=['olt_num']),
        ]


class OltInfoWG(models.Model):
    olt_num = models.CharField(max_length=10, primary_key=True)
    district = models.CharField(max_length=10)
    olt_zh = models.CharField(max_length=100)
    state = models.CharField(max_length=20, null=True)
    olt_type = models.CharField(max_length=10, null=True)
    ip = models.GenericIPAddressField()

    class Meta:
        db_table = 'MR_REC_olt_info_wg'
        indexes = [
            models.Index(fields=['ip']),
        ]


class GroupClientIPSegment(models.Model):
    ip = models.GenericIPAddressField(protocol='both', unique=True)
    # ip_state = models.BooleanField(default=False)
    ip_state = models.SmallIntegerField(default=0)  # 0未使用 1已用 2下沉地址已用
    segment = models.GenericIPAddressField(protocol='both')
    mask = models.PositiveSmallIntegerField()
    segment_state = models.BooleanField(default=False)
    subnet_gateway = models.GenericIPAddressField(protocol='both', null=True)
    subnet_mask = models.PositiveSmallIntegerField(null=True)
    ip_func = models.CharField(max_length=2, null=True)

    class Meta:
        db_table = 'MR_REC_group_client_ip_segment'
        indexes = [
            models.Index(fields=['segment']),
            models.Index(fields=['subnet_gateway']),
        ]

class GroupClientIpReserve(models.Model):
    subnet_gateway = models.GenericIPAddressField(protocol='both')
    subnet_mask = models.PositiveSmallIntegerField()
    reserved_cnt = models.PositiveIntegerField()
    reserved_person = models.CharField(max_length=20)
    client_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=11)   # 联系电话
    reserved_time = models.DateTimeField()

    class Meta:
        db_table = 'MR_REC_group_client_ip_reserve'
        indexes = [
            models.Index(fields=['subnet_gateway']),
        ]

        
class GroupClientPublicGateway(models.Model):
    gateway = models.GenericIPAddressField(protocol='both')
    olt_cnt = models.PositiveIntegerField(default=0)
    olts = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'MR_STS_group_client_public_gateway'


class SwVlan(models.Model):
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=30)
    vlan = models.PositiveIntegerField()

    class Meta:
        db_table = 'MR_REC_sw_vlan'

