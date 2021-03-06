from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from watchdog.models import Device
from inspection.models import OpticalMoudleDiff, PortErrorDiff, OneWayDevice, NatPoolUsage, LinkPingHourAggregate
from networkresource.models import IpRecord, IPAllocation, IPMod
import datetime
from django.utils import timezone
from django.db.models import Count, Q, Max, Sum, F
from funcpack.funcs import getDateRange


def register(request):
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():   # is_valid方法会执行forms内的clean的方法
            username = reg_form.cleaned_data['username']
            first_name = reg_form.cleaned_data['first_name']    # 中文名
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(
                username=username, email=email, password=password, first_name=first_name)
            user.save()
            # 创建用户后自动登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            # from 通过html的url设置的get请求获得
            # reverse反向解析到doahboard的链接
            return redirect(request.GET.get('from', reverse('dashboard')))
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
            # reverse反向解析到doahboard的链接
            return redirect(request.GET.get('from', reverse('dashboard')))
    else:   # 如果非post请求
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    # reverse反向解析到doahboard的链接
    return redirect(request.GET.get('from', reverse('dashboard')))


def dashboard(request):
    context = {}
    # 设备信息
    device_count = Device.objects.all().count()
    device_ipman_count = Device.objects.filter(
        device_network__icontains='IPMAN').count()
    device_cmnet_count = Device.objects.filter(
        device_network__icontains='CMNET').count()
    device_oth_count = device_count-device_ipman_count-device_cmnet_count
    context['device_count'] = device_count
    context['device_ipman_count'] = device_ipman_count
    context['device_cmnet_count'] = device_cmnet_count
    context['device_oth_count'] = device_oth_count
    # 模块信息
    moudle_new_count = OpticalMoudleDiff.objects.filter(
        status='NEW', record_time__range=getDateRange(-1)).count()
    moudle_miss_count = OpticalMoudleDiff.objects.filter(
        status='MISS', record_time__range=getDateRange(-1)).count()
    moudle_ch_count = OpticalMoudleDiff.objects.filter(
        status='CH', record_time__range=getDateRange(-1)).count()
    context['moudle_new_count'] = moudle_new_count
    context['moudle_miss_count'] = moudle_miss_count
    context['moudle_ch_count'] = moudle_ch_count
    # IP地址信息
    ip_count = IpRecord.objects.all().count()
    ip_private_count = IpRecord.objects.filter(ip_type='private').count()
    ip_public_count = IpRecord.objects.filter(
        ip_type__icontains='public').count()
    context['ip_count'] = ip_count
    context['ip_private_count'] = ip_private_count
    context['ip_public_count'] = ip_public_count
    if ip_count != 0:
        context['ip_private_ratio'] = ip_private_count/ip_count*100
        context['ip_public_ratio'] = ip_public_count/ip_count*100
    else:
        context['ip_private_ratio'] = 0
        context['ip_public_ratio'] = 0
    # 端口错包信息
    crc_port_count = PortErrorDiff.objects.filter(
        stateCRC__gt=0, record_time__range=getDateRange(-2)).count()
    crc_max_speed = PortErrorDiff.objects.filter(
        record_time__range=getDateRange(-2)).aggregate(Max('stateCRC'))
    ipv4head_port_count = PortErrorDiff.objects.filter(
        stateIpv4HeadError__gt=0, record_time__range=getDateRange(-2)).count()
    ipv4head_max_speed = PortErrorDiff.objects.filter(
        record_time__range=getDateRange(-2)).aggregate(Max('stateIpv4HeadError'))
    context['crc_port_count'] = crc_port_count
    context['crc_max_speed'] = crc_max_speed
    context['ipv4head_port_count'] = ipv4head_port_count
    context['ipv4head_max_speed'] = ipv4head_max_speed
    # 单通设备检查
    oneway_count = OneWayDevice.objects.filter(record_time__range=getDateRange(-1)).count()
    oneway_devices = OneWayDevice.objects.filter(record_time__range=getDateRange(-1)).values('device_name').annotate(port_cnt=Sum('port')).order_by('-port_cnt')
    context['oneway_devices'] = oneway_devices
    context['oneway_count'] = oneway_count
    # nat地址池
    heavy_load_pair_devices = NatPoolUsage.objects.filter(record_time__range=getDateRange(-2)).annotate(nat_total=(F('device1_nat_usage')+F('device2_nat_usage'))).order_by(F('nat_total').desc())[0:5]
    context['heavy_load_pair_devices'] = heavy_load_pair_devices
    # ping
    cost_hour_group_list = LinkPingHourAggregate.objects.all().order_by('id')
    l = {}
    for cost_hour in cost_hour_group_list:
        temp = []
        for f in cost_hour._meta.fields[2::]:
            val = cost_hour.serializable_value(f.attname)
            temp.append(str(val))
        l[cost_hour.direction] = ','.join(temp)
    context['cost_hour_group_list'] = l
    # 业务开通情况
    # 当天情况
    ip_mod_aggregate = IPMod.objects.filter(mod_time__range=getDateRange(-1)).values('mod_type').annotate(Count('ip', distinct=True)).order_by()
    ip_alloc_num = IPAllocation.objects.filter(alc_time__range=getDateRange(-1)).values('ip').annotate(Count('ip', distinct=True)).order_by().count()
    context['ip_mod_aggregate'] = ip_mod_aggregate
    context['ip_alloc_num'] = ip_alloc_num
    # 历史7天开通情况
    ip_mod_7day_raw_query = '''
    SELECT id, mod_type,
    sum(if(date_format(DATE_SUB(CURDATE(), INTERVAL 6 DAY), '%%Y-%%m-%%d')=mt, 1, 0)) AS d0,
    sum(if(date_format(DATE_SUB(CURDATE(), INTERVAL 5 DAY), '%%Y-%%m-%%d')=mt, 1, 0)) AS d1,
    sum(if(date_format(DATE_SUB(CURDATE(), INTERVAL 4 DAY), '%%Y-%%m-%%d')=mt, 1, 0)) AS d2,
    sum(if(date_format(DATE_SUB(CURDATE(), INTERVAL 3 DAY), '%%Y-%%m-%%d')=mt, 1, 0)) AS d3,
    sum(if(date_format(DATE_SUB(CURDATE(), INTERVAL 2 DAY), '%%Y-%%m-%%d')=mt, 1, 0)) AS d4,
    sum(if(date_format(DATE_SUB(CURDATE(), INTERVAL 1 DAY), '%%Y-%%m-%%d')=mt, 1, 0)) AS d5,
    sum(if(date_format(DATE_SUB(CURDATE(), INTERVAL 0 DAY), '%%Y-%%m-%%d')=mt, 1, 0)) AS d6
    FROM (SELECT id, ip, mod_type, DATE_FORMAT(mod_time, '%%Y-%%m-%%d') AS mt FROM MR_REC_ip_mod_record GROUP BY ip, mod_type, mt) AS mod_agg
    GROUP BY mod_type
    ORDER BY mod_type ASC 
    '''
    ip_mod_dict = {}
    ip_mod_7day_result = IPMod.objects.raw(ip_mod_7day_raw_query)
    for mod_data in ip_mod_7day_result:
        temp = []
        for f in ip_mod_7day_result.columns[2::]:
            val = mod_data.serializable_value(f)
            temp.append(str(val))
        ip_mod_dict[mod_data.mod_type] = ','.join(temp)
    context['ip_mod_dict'] = ip_mod_dict
    ip_alloc_7day_raw_query = '''
    SELECT id, COUNT(DISTINCT(ip)) AS cnt, DATE_FORMAT(alc_time, '%%Y-%%m-%%d') AS alct 
    FROM mr_rec_ip_allocation
    WHERE alc_time >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
    GROUP BY alc_time ORDER BY alct ASC 
    '''
    # alloc_date_list = []
    # ip_alloc_dict = {}
    # temp_ip_alloc_list = []
    # ip_alloc_7day_result = IPAllocation.objects.raw(ip_alloc_7day_raw_query)
    # for alloc_data in ip_alloc_7day_result:
    #     alloc_date_list.append(alloc_data.alct)
    #     temp_ip_alloc_list.append(str(alloc_data.cnt))
    # context['ip_alloc_dict'] = {'alloc': ','.join(temp_ip_alloc_list)}
    # 其他
    today_time = datetime.datetime.now()
    context['time_begin'] = '%d-%d-%d+00:00:00' % (
        today_time.year, today_time.month, today_time.day)
    context['time_end'] = '%d-%d-%d+23:59:59' % (
        today_time.year, today_time.month, today_time.day)

    return render(request, 'dashboard.html', context)



