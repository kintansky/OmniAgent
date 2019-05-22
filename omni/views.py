from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from watchdog.models import Device
from inspection.models import OpticalMoudleDiff, PortErrorDiff
from networkresource.models import IpmanResource, IpRecord
import datetime
from django.utils import timezone
from django.db.models import Count, Q, Max
from funcpack.funcs import dumpOlt2Json

def register(request):
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():   # is_valid方法会执行forms内的clean的方法
            username = reg_form.cleaned_data['username']
            first_name = reg_form.cleaned_data['first_name']    # 中文名
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            user.save()
            # 创建用户后自动登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            # from 通过html的url设置的get请求获得
            return redirect(request.GET.get('from', reverse('dashboard')))  # reverse反向解析到doahboard的链接
    else:   # 如果非post请求
        reg_form = RegisterForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():   # is_valid方法会执行forms内的clean的方法
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('dashboard')))  # reverse反向解析到doahboard的链接
    else:   # 如果非post请求
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('dashboard')))  # reverse反向解析到doahboard的链接

def dashboard(request):
    context = {}
    # 设备信息
    device_count = Device.objects.all().count()
    device_ipman_count = Device.objects.filter(device_network__icontains='IPMAN').count()
    device_cmnet_count = Device.objects.filter(device_network__icontains='CMNET').count()
    device_oth_count = device_count-device_ipman_count-device_cmnet_count
    context['device_count'] = device_count
    context['device_ipman_count'] = device_ipman_count
    context['device_cmnet_count'] = device_cmnet_count
    context['device_oth_count'] = device_oth_count
    # 模块信息
    today_time = datetime.datetime.now()
    time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
    time_begin = time_end + timezone.timedelta(days=-1)
    moudle_new_count = OpticalMoudleDiff.objects.filter(status='NEW', record_time__range=(time_begin, time_end)).count()
    moudle_miss_count = OpticalMoudleDiff.objects.filter(status='MISS', record_time__range=(time_begin, time_end)).count()
    moudle_ch_count = OpticalMoudleDiff.objects.filter(status='CH', record_time__range=(time_begin, time_end)).count()
    context['moudle_new_count'] = moudle_new_count
    context['moudle_miss_count'] = moudle_miss_count
    context['moudle_ch_count'] = moudle_ch_count
    # IP地址信息
    ip_count = IpRecord.objects.all().count()
    ip_private_count = IpRecord.objects.filter(ip_type='private').count()
    ip_public_count = IpRecord.objects.filter(ip_type__icontains='public').count()
    context['ip_count'] = ip_count
    context['ip_private_count'] = ip_private_count
    context['ip_public_count'] = ip_public_count
    context['ip_private_ratio'] = ip_private_count/ip_count*100
    context['ip_public_ratio'] = ip_public_count/ip_count*100
    # 端口错包信息
    crc_port_count = PortErrorDiff.objects.filter(stateCRC__gt=0, record_time__range=(time_end+ timezone.timedelta(days=-2), time_end)).count()
    crc_max_speed = PortErrorDiff.objects.filter(record_time__range=(time_end+ timezone.timedelta(days=-2), time_end)).aggregate(Max('stateCRC'))
    ipv4head_port_count = PortErrorDiff.objects.filter(stateIpv4HeadError__gt=0, record_time__range=(time_end+ timezone.timedelta(days=-2), time_end)).count()
    ipv4head_max_speed = PortErrorDiff.objects.filter(record_time__range=(time_end+ timezone.timedelta(days=-2), time_end)).aggregate(Max('stateIpv4HeadError'))
    context['crc_port_count'] = crc_port_count
    context['crc_max_speed'] = crc_max_speed
    context['ipv4head_port_count'] = ipv4head_port_count
    context['ipv4head_max_speed'] = ipv4head_max_speed

    # 其他
    context['time_begin'] = '%d-%d-%d+00:00:00' % (today_time.year, today_time.month, today_time.day)
    context['time_end'] = '%d-%d-%d+23:59:59' % (today_time.year, today_time.month, today_time.day)
    
    return render(request, 'dashboard.html', context)

def device_detail(request, device_name):
    device = get_object_or_404(Device, device_name=device_name)
    # slot_brief = IpmanResource.objects.filter(device_name=device_name).values_list('slot').annotate(allports=Count('slot'), upports=Count('port_status', filter=Q(port_status='Up'))).order_by('slot')
    rawQueryCmd = "SELECT nt.id, nt.slot, COUNT(nt.slot) AS allports, \
                    COUNT(case when nt.port_status = 'Up' then nt.port_status else NULL END ) AS upports, \
                    SUM(case when nt.stateCRC > 0 then nt.stateCRC ELSE 0 END ) AS crc \
                FROM (\
                    SELECT ni.id, ni.slot, ni.port, ni.brand_width, \
                        ni.port_status, ni.port_phy_status, ni.logic_port, ni.port_description, np.stateCRC \
                    FROM networkresource_ipmanresource AS ni \
                    LEFT JOIN networkresource_porterrordiff as np \
                    ON np.device_name = ni.device_name AND np.port = ni.port AND np.record_time BETWEEN %s AND %s \
                    WHERE ni.device_name = %s) AS nt \
                GROUP BY nt.slot"
    today_time = timezone.datetime.now()
    time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
    time_begin = time_end + timezone.timedelta(days=-2)
    rawQueryData = (time_begin, time_end, device_name)
    slot_brief = IpmanResource.objects.raw(rawQueryCmd, rawQueryData)
    port_up_count = IpmanResource.objects.filter(device_name=device_name, port_status__icontains='up').count()
    port_down_count = IpmanResource.objects.filter(device_name=device_name).count() - port_up_count
    # 关系查询需要修改model的建立外键关系，或者使用raw query
    # rawQueryCmd = 'SELECT id, port_description FROM cmdb.networkresource_ipmanresource WHERE device_name = %s AND port_description REGEXP "dT:.*?"'
    # oltList = IpmanResource.objects.raw(rawQueryCmd, (device_name,))
    # olts = set()
    # for olt in oltList:
    #     olts.add(olt.port_description.split(':')[1])
    # oltJson = dumpOlt2Json(olts, device_name)

    context = {}
    context['device'] = device
    context['slot_brief'] = slot_brief
    context['port_up_count'] = port_up_count
    context['port_down_count'] = port_down_count
    # context['networkjson'] = oltJson
    return render(request, 'device_detail.html', context)