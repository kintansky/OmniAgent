from django.shortcuts import render, get_object_or_404
# 将路径加入sys.path, 否则找不到models
import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname('omni')), 'watchdog'))
sys.path.insert(0, join(abspath(dirname('omni')), 'inspection'))
sys.path.insert(0, join(abspath(dirname('omni')), 'networkresource'))
from watchdog.models import Device
from inspection.models import OpticalMoudleDiff
from networkresource.models import IpmanResource, IpRecord
import datetime
from django.utils import timezone

def dashboard(request):
    device_count = Device.objects.all().count()
    device_ipman_count = Device.objects.filter(device_network__icontains='IPMAN').count()
    device_cmnet_count = Device.objects.filter(device_network__icontains='CMNET').count()
    device_oth_count = device_count-device_ipman_count-device_cmnet_count
    
    today_time = datetime.datetime.now()
    time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
    time_begin = time_end + timezone.timedelta(days=-1)
    moudle_new_count = OpticalMoudleDiff.objects.filter(status='NEW', record_time__range=(time_begin, time_end)).count()
    moudle_miss_count = OpticalMoudleDiff.objects.filter(status='MISS', record_time__range=(time_begin, time_end)).count()
    moudle_ch_count = OpticalMoudleDiff.objects.filter(status='CH', record_time__range=(time_begin, time_end)).count()

    ip_count = IpRecord.objects.all().count()

    context = {}
    context['device_count'] = device_count
    context['device_ipman_count'] = device_ipman_count
    context['device_cmnet_count'] = device_cmnet_count
    context['device_oth_count'] = device_oth_count
    context['moudle_new_count'] = moudle_new_count
    context['moudle_miss_count'] = moudle_miss_count
    context['moudle_ch_count'] = moudle_ch_count
    context['time_begin'] = '%d-%d-%d+00:00:00' % (today_time.year, today_time.month, today_time.day)
    context['time_end'] = '%d-%d-%d+23:59:59' % (today_time.year, today_time.month, today_time.day)
    context['ip_count'] = ip_count
    return render(request, 'dashboard.html', context)

def device_detail(request, device_name):
    device = get_object_or_404(Device, device_name=device_name)
    device_ports = IpmanResource.objects.filter(device_name=device_name)
    port_up_count = IpmanResource.objects.filter(device_name=device_name, port_status__icontains='up').count()
    port_down_count = IpmanResource.objects.filter(device_name=device_name).count() - port_up_count
    # 关系查询需要修改model的建立外键关系
    
    context = {}
    context['device'] = device
    context['device_ports'] = device_ports
    context['port_up_count'] = port_up_count
    context['port_down_count'] = port_down_count
    return render(request, 'device_detail.html', context)