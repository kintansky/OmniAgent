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
        db_table = 'OM_REP_optical_moudle_diff'
        ordering = ['-record_time']
        

class PortErrorFullRecord(models.Model):
    device = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    crc = models.IntegerField()
    ipv4_head = models.IntegerField()
    record_time = models.DateTimeField()

    class Meta:
        db_table = 'OM_REC_port_error_record'
        ordering = ['-record_time']


class PortErrorDiff(models.Model):
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    nowCRC = models.IntegerField(null=True)
    nowIpv4HeaderError = models.IntegerField(null=True)
    everCRC = models.IntegerField(null=True)
    everIpv4HeaderError = models.IntegerField(null=True)
    stateCRC = models.FloatField(null=True)  # CRC每小时增速
    stateIpv4HeadError = models.FloatField(null=True)    # head每小时增速
    record_time = models.DateTimeField(auto_now_add=True)
    fix_status = models.BooleanField(default=False, null=True)  # 修复标记位，1代表该条记录已修复

    class Meta:
        db_table = 'OM_REP_port_error_diff'
        # app_label = 'networkresource'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['device_name']),
            models.Index(fields=['port']),
        ]


class FixRecordBase(models.Model):
    problem_type = models.CharField(max_length=40, null=True)
    problem_detail = models.TextField(null=True)
    begin_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    # worker = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    worker = models.CharField(max_length=100)
    status = models.BooleanField(default=False)    # 标记是否已经完成处理
    claim = models.BooleanField(default=True)    # 用户认领端口，默认True，即建立记录就认领，处理完重新设置为False

    class Meta:
        abstract = True


class PortErrorFixRecord(FixRecordBase):
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    # problem_type = models.CharField(max_length=40, null=True)
    # problem_detail = models.TextField(null=True)
    # begin_time = models.DateTimeField(auto_now_add=True)
    # end_time = models.DateTimeField(null=True)
    # worker = models.CharField(max_length=100)
    # status = models.BooleanField(default=False)    # 标记是否已经完成处理
    # claim = models.BooleanField(default=True)    # 用户认领端口，默认True，即建立记录就认领，处理完重新设置为False

    class Meta:
        db_table = 'OM_REC_port_error_fix_record'

'''
PortErrorDiff 记录时初始状态fix_status=0
    端口未处理
    PortErrorFixRecord：用户未认领，无记录
    端口已认领
    PortErrorFixRecord：用户认领claim=1，初始记录status=0
    端口已修复
    PortErrorFixRecord：用户认领claim=0，初始记录status=1，同时PortErrorDiff fix_status=1表明已修复，同一个端口，claim=1的只会有一条
PortErrorDiff 记录状态fix_status=1
    基于以上逻辑
    PortErrorFixRecord：肯定存在status=1，claim=0的记录
    如果有status=0，claim=1的记录肯定是发生在该条PortErrorDiff条目记录时间之后，即新发现的记录

如果出现新PortErrorDiff记录
    如果旧PortErrorDiff记录未修复，PortErrorFixRecord.claim=1的会一直标记PortErrorDiff处于被认领状态
    旧PortErrorDiff记录已修复或不存在，PortErrorFixRecord.claim=0，则可以通过claim位区分是否需要被认领处理
'''


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
        db_table = 'OM_REC_port_perf'
        # app_label = 'networkresource'
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
        db_table = 'OM_REP_oneway_device'
        ordering = ['-record_time']
        indexes = [
            models.Index(fields=['device_name']),
            models.Index(fields=['port']),
        ]


class OneWayDeviceTag(models.Model):
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    delay_count = models.PositiveSmallIntegerField(null=True)
    tag = models.CharField(max_length=10)
    tag_user = models.CharField(max_length=100)
    tag_time = models.DateTimeField()

    class Meta:
        db_table = 'OM_REC_oneway_device_tag'


# class OneWayDeviceFixRecord(FixRecordBase):
#     device_name = models.CharField(max_length=255)
#     port = models.CharField(max_length=40)


class NatPoolUsage(models.Model):
    device1 = models.CharField(max_length=255)
    # device1_nat_usage = models.DecimalField(max_digits=5, decimal_places=2)   # mysql-connector bug, raise decimal cant be deocded
    device1_nat_usage = models.FloatField()
    device2 = models.CharField(max_length=255)
    # device2_nat_usage = models.DecimalField(max_digits=5, decimal_places=2)
    device2_nat_usage = models.FloatField()
    record_time = models.DateTimeField()

    class Meta:
        db_table = 'OM_REC_nat_pool_usage'
        ordering = ['-record_time']


class LinkPingTest(models.Model):
    source_device = models.CharField(max_length=255)
    target_device = models.CharField(max_length=255)
    target_ip = models.GenericIPAddressField()
    loss = models.IntegerField()
    cost = models.IntegerField()
    record_time = models.DateTimeField()

    class Meta:
        db_table = 'OM_REP_ping_test'


class LinkPingHourAggregate(models.Model):
    direction = models.CharField(max_length=20)
    h0 = models.FloatField()
    h1 = models.FloatField()
    h2 = models.FloatField()
    h3 = models.FloatField()
    h4 = models.FloatField()
    h5 = models.FloatField()
    h6 = models.FloatField()
    h7 = models.FloatField()
    h8 = models.FloatField()
    h9 = models.FloatField()
    h10 = models.FloatField()
    h11 = models.FloatField()
    h12 = models.FloatField()
    h13 = models.FloatField()
    h14 = models.FloatField()
    h15 = models.FloatField()
    h16 = models.FloatField()
    h17 = models.FloatField()
    h18 = models.FloatField()
    h19 = models.FloatField()
    h20 = models.FloatField()
    h21 = models.FloatField()
    h22 = models.FloatField()
    h23 = models.FloatField()

    class Meta:
        db_table = 'OM_REP_ping_hour_aggregate'


class LinkPingCostStepAggregate(models.Model):
    step = models.PositiveSmallIntegerField()
    link_cnt = models.PositiveIntegerField()

    class Meta:
        db_table = 'OM_REP_ping_cost_step_aggregate'