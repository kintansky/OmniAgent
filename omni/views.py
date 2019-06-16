from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from watchdog.models import Device
from inspection.models import OpticalMoudleDiff, PortErrorDiff, OneWayDevice, NatPoolUsage
from networkresource.models import IpRecord
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
    # today_time = datetime.datetime.now()
    # time_end = timezone.datetime(year=today_time.year, month=today_time.month,
    #                              day=today_time.day, hour=23, minute=59, second=59)
    # time_begin = time_end + timezone.timedelta(days=-1)
    time_range = getDateRange(-1)
    moudle_new_count = OpticalMoudleDiff.objects.filter(
        status='NEW', record_time__range=time_range).count()
    moudle_miss_count = OpticalMoudleDiff.objects.filter(
        status='MISS', record_time__range=time_range).count()
    moudle_ch_count = OpticalMoudleDiff.objects.filter(
        status='CH', record_time__range=time_range).count()
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
    time_range = getDateRange(-2)
    crc_port_count = PortErrorDiff.objects.filter(
        stateCRC__gt=0, record_time__range=time_range).count()
    crc_max_speed = PortErrorDiff.objects.filter(
        record_time__range=time_range).aggregate(Max('stateCRC'))
    ipv4head_port_count = PortErrorDiff.objects.filter(
        stateIpv4HeadError__gt=0, record_time__range=time_range).count()
    ipv4head_max_speed = PortErrorDiff.objects.filter(
        record_time__range=time_range).aggregate(Max('stateIpv4HeadError'))
    context['crc_port_count'] = crc_port_count
    context['crc_max_speed'] = crc_max_speed
    context['ipv4head_port_count'] = ipv4head_port_count
    context['ipv4head_max_speed'] = ipv4head_max_speed
    # 单通设备检查
    time_range = getDateRange(-1)
    oneway_count = OneWayDevice.objects.filter(record_time__range=time_range).count()
    oneway_devices = OneWayDevice.objects.filter(record_time__range=time_range).values('device_name').annotate(port_cnt=Sum('port')).order_by('-port_cnt')
    context['oneway_devices'] = oneway_devices
    context['oneway_count'] = oneway_count
    # nat地址池
    time_range = getDateRange(-1)
    # 注意修改测试日期
    heavy_load_pair_devices = NatPoolUsage.objects.filter(record_time__range=('2019-06-13 00:00:00', '2019-06-14 00:00:00')).annotate(nat_total=(F('device1_nat_usage')+F('device2_nat_usage'))).order_by(F('nat_total').desc())[0:5]
    context['heavy_load_pair_devices'] = heavy_load_pair_devices
    # 其他
    today_time = datetime.datetime.now()
    context['time_begin'] = '%d-%d-%d+00:00:00' % (
        today_time.year, today_time.month, today_time.day)
    context['time_end'] = '%d-%d-%d+23:59:59' % (
        today_time.year, today_time.month, today_time.day)

    return render(request, 'dashboard.html', context)



