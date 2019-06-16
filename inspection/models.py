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
        # app_label = 'networkresource'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['device_name']),
            models.Index(fields=['port']),
        ]


class PortErrorFixRecord(models.Model):
    # target = models.ForeignKey(PortErrorDiff, on_delete=models.DO_NOTHING)
    device_name = models.CharField(max_length=255)
    port = models.CharField(max_length=40)
    problem_type = models.CharField(max_length=40, null=True)
    problem_detail = models.TextField(null=True)
    begin_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    # worker = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    worker = models.CharField(max_length=100)
    status = models.BooleanField(default=False)    # 标记是否已经完成处理
    claim = models.BooleanField(default=True)    # 用户认领端口，默认True，即建立记录就认领，处理完重新设置为False

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
        ordering = ['-record_time']
        indexes = [
            models.Index(fields=['device_name']),
            models.Index(fields=['port']),
        ]
    

class NatPoolUsage(models.Model):
    device1 = models.CharField(max_length=255)
    device1_nat_usage = models.DecimalField(max_digits=5, decimal_places=2)
    device2 = models.CharField(max_length=255)
    device2_nat_usage = models.DecimalField(max_digits=5, decimal_places=2)
    record_time = models.DateTimeField()

    class Meta:
        ordering = ['-record_time']
