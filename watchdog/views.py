from django.shortcuts import render, get_object_or_404
from .models import Device, DeviceManufactor
from .forms import AddDeviceForm
from networkresource.models import IpmanResource
from inspection.models import NatPoolUsage
from django.utils import timezone
# 下面为了引入funcpack的公共函数
from funcpack.funcs import pages, dumpOlt2Json
from django.db.models import Q

# Create your views here.

def device_list(request):
    device_all_list = Device.objects.all()
    page_of_objects, page_range = pages(request, device_all_list)

    context = {}
    context['devices'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['count'] = Device.objects.all().count()
    return render(request, 'device_list.html', context)


def search_device(request):
    ip_address = request.GET.get('ip_address', '')
    device_name = request.GET.get('device_name', '')
    if ip_address != '' and device_name == '':
        device_all_list = Device.objects.filter(device_ip=ip_address)
    elif device_name != '' and ip_address == '':
        device_all_list = Device.objects.filter(
            device_name__icontains=device_name)
    elif ip_address != '' and device_name != '':
        device_all_list = Device.objects.filter(
            device_name__icontains=device_name, device_ip=ip_address)
    else:
        device_all_list = Device.objects.all()

    page_of_objects, page_range = pages(request, device_all_list)

    context = {}
    context['devices'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['search_device_name'] = device_name
    context['search_ip_address'] = ip_address
    context['count'] = Device.objects.all().count()

    return render(request, 'device_list.html', context)


def add_device(request):
    status = 0
    if request.method == 'POST':
        add_device_form = AddDeviceForm(request.POST)
        if add_device_form.is_valid():
            NewDevice = Device()
            NewDevice.device_name = add_device_form.cleaned_data['device_name']
            NewDevice.device_ip = add_device_form.cleaned_data['device_ip']
            dm = add_device_form.cleaned_data['device_manufactor']
            NewDevice.device_manufactor = get_object_or_404(
                DeviceManufactor, manufactor_name=dm)
            NewDevice.device_network = add_device_form.cleaned_data['device_network']
            NewDevice.login_user = add_device_form.cleaned_data['login_user']
            NewDevice.login_port = add_device_form.cleaned_data['login_port']
            NewDevice.login_password = add_device_form.cleaned_data['login_password']
            NewDevice.save()
            status = 1
            add_device_form = AddDeviceForm()
        else:
            status = -1
    else:
        add_device_form = AddDeviceForm()

    context = {}
    context['add_device_form'] = add_device_form
    context['status'] = status
    return render(request, 'add_device.html', context)


def device_detail(request, device_name):
    context = {}
    device = get_object_or_404(Device, device_name=device_name)
    context['device'] = device
    # slot_brief = IpmanResource.objects.filter(device_name=device_name).values_list('slot').annotate(allports=Count('slot'), upports=Count('port_status', filter=Q(port_status='Up'))).order_by('slot')
    rawQueryCmd = "SELECT nt.id, nt.slot, COUNT(nt.slot) AS allports, \
                    COUNT(case when nt.port_status = 'Up' then nt.port_status else NULL END ) AS upports, \
                    SUM(case when nt.stateCRC > 0 then nt.stateCRC ELSE 0 END ) AS crc \
                FROM (\
                    SELECT ni.id, ni.slot, ni.port, ni.brand_width, \
                        ni.port_status, ni.port_phy_status, ni.logic_port, ni.port_description, np.stateCRC \
                    FROM MR_REC_ipman_resource AS ni \
                    LEFT JOIN OM_REP_port_error_diff as np \
                    ON np.device_name = ni.device_name AND np.port = ni.port AND np.record_time BETWEEN %s AND %s \
                    WHERE ni.device_name = %s) AS nt \
                GROUP BY nt.slot ORDER BY nt.slot"
    today_time = timezone.datetime.now()
    time_end = timezone.datetime(year=today_time.year, month=today_time.month,
                                 day=today_time.day, hour=23, minute=59, second=59)
    time_begin = time_end + timezone.timedelta(days=-2)
    rawQueryData = (time_begin, time_end, device_name)
    slot_brief = IpmanResource.objects.raw(rawQueryCmd, rawQueryData)
    port_up_count = IpmanResource.objects.filter(
        device_name=device_name, port_status__icontains='up').count()
    port_down_count = IpmanResource.objects.filter(
        device_name=device_name).count() - port_up_count
    context['slot_brief'] = slot_brief
    context['port_up_count'] = port_up_count
    context['port_down_count'] = port_down_count
    # 网络下联拓扑
    rawQueryCmd = 'SELECT id, port_description FROM MR_REC_ipman_resource WHERE device_name = %s AND port_description REGEXP "dT:.*?"'
    oltList = IpmanResource.objects.raw(rawQueryCmd, (device_name,))
    olts = set()
    for olt in oltList:
        olts.add(olt.port_description.split(':')[1])
    oltJson = dumpOlt2Json(olts, device_name)
    context['networkjson'] = oltJson
    # print(oltJson)
    # nat地址利用率，只有bras和bng有
    if '-BNG' in device_name or '-BRAS' in device_name:
        natpool_usage = NatPoolUsage.objects.filter(Q(device1=device_name) | Q(device2=device_name)).order_by('-record_time')[0]
        pair_device1 = natpool_usage.device1.split('-')[-2] + '-' + natpool_usage.device1.split('-')[-3]
        pair_device2 = natpool_usage.device2.split('-')[-2] + '-' + natpool_usage.device2.split('-')[-3]
        context['natpool_usage'] = natpool_usage
        context['pair_device1'] = pair_device1
        context['pair_device2'] = pair_device2
    
    return render(request, 'device_detail.html', context)