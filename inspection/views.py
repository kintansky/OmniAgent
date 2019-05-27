from django.shortcuts import render, redirect
from .models import OpticalMoudleDiff, PortErrorDiff, OneWayDevice
from django.utils import timezone
from .forms import MoudleSearchForm, PortErrorSearchForm, OneWaySearchForm
from funcpack.funcs import pages, getDateRange, exportXls, rawQueryExportXls
from django.http import FileResponse, JsonResponse
# from django.core import serializers
import json


# Create your views here.

# 光模块检查模块
def moudle_list(request):
    # 默认展示前3天数据
    moudle_all_list = OpticalMoudleDiff.objects.filter(
        record_time__range=getDateRange(-3))
    # moudle_all_list = OpticalMoudleDiff.objects.all()

    page_of_objects, page_range = pages(request, moudle_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['moudle_search_form'] = MoudleSearchForm()
    return render(request, 'moudle_list.html', context)


def search_moudle(request):
    moudle_search_form = MoudleSearchForm(request.GET)
    if moudle_search_form.is_valid():
        device_name = moudle_search_form.cleaned_data['device_name']
        status = moudle_search_form.cleaned_data['status']
        time_begin = moudle_search_form.cleaned_data['time_begin']
        time_end = moudle_search_form.cleaned_data['time_end']
        time_range = (time_begin, time_end)
        if device_name != '':
            moudle_all_list = OpticalMoudleDiff.objects.filter(
                device_name__icontains=device_name, status__contains=status, record_time__range=time_range)
        elif status != '':
            moudle_all_list = OpticalMoudleDiff.objects.filter(
                status=status, record_time__range=time_range)
        else:
            moudle_all_list = OpticalMoudleDiff.objects.filter(
                record_time__range=time_range)
    else:
        context = {}
        context['moudle_search_form'] = moudle_search_form
        return render(request, 'moudle_list.html', context)
    page_of_objects, page_range = pages(request, moudle_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['search_device_name'] = device_name
    context['search_status'] = status
    context['time_begin'] = timezone.datetime.strftime(
        time_range[0], '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(
        time_range[1], '%Y-%m-%d+%H:%M:%S')
    context['moudle_search_form'] = moudle_search_form

    return render(request, 'moudle_list.html', context)


def export_moudle(request):
    device_name = request.GET.get('device_name', '')
    status = request.GET.get('status', '')
    time_begin = request.GET.get('time_begin', '')
    print(request.GET.get('time_begin'))
    time_end = request.GET.get('time_end', '')
    print(request.GET.get('time_end'))

    if time_begin == '' or time_end == '':
        # 默认下载前一天的数据
        time_range = getDateRange(-1)
    else:
        time_begin = timezone.datetime.strptime(
            time_begin, '%Y-%m-%d %H:%M:%S')
        time_end = timezone.datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
        time_range = (time_begin, time_end)
        print(time_range)
    if device_name == status == '':
        moudle_all_list = OpticalMoudleDiff.objects.filter(
            record_time__range=time_range)
    else:
        if device_name != '':   # device_name != '' status == ''
            moudle_all_list = OpticalMoudleDiff.objects.filter(
                device_name__icontains=device_name, record_time__range=time_range)
        elif status != '':  # device_name == '' status != ''
            moudle_all_list = OpticalMoudleDiff.objects.filter(
                status=status, record_time__range=time_range)
        else:
            moudle_all_list = OpticalMoudleDiff.objects.filter(
                record_time__range=time_range)
    output = exportXls(OpticalMoudleDiff._meta.fields,
                       moudle_all_list, 'record_time')
    response = FileResponse(open(output, 'rb'), as_attachment=True,
                            filename="moudle_result.xls")  # 使用Fileresponse替代以上两行
    return response


# 端口质量模块
# port error 采用rawquery做连接查询，取出其他关联信息 用于请求CRC+光功率的信息
__PORTERROR_QUERY = "\
    SELECT error_info.*, npp.* FROM (\
        SELECT np.*, ni.port_description, ni.port_status \
            FROM networkresource_porterrordiff as np \
            LEFT JOIN networkresource_ipmanresource AS ni \
            ON np.device_name = ni.device_name AND np.port = ni.port \
            WHERE np.record_time between %s AND %s\
        ) AS error_info \
    LEFT JOIN (\
        SELECT device_name, `port`, tx_now_power, tx_high_warm, tx_low_warm, tx_state, rx_now_power, rx_high_warm, rx_low_warm, rx_state, utility_in, utility_out, record_time \
            FROM cmdb.networkresource_portperf \
            WHERE record_time BETWEEN %s AND %s\
        ) AS npp \
    ON error_info.device_name = npp.device_name AND error_info.port = npp.port \
    AND DATE_FORMAT(error_info.record_time, '%Y-%m-%d') = DATE_FORMAT(npp.record_time, '%Y-%m-%d') \
"


def __queryline(order_field):
    if order_field == 'crc':
        porterror_query = __PORTERROR_QUERY + 'ORDER BY -error_info.stateCRC'
    elif order_field == 'head':
        porterror_query = __PORTERROR_QUERY + 'ORDER BY -error_info.stateIpv4HeadError'
    return porterror_query


def port_error_list(request):
    order_field = request.GET.get('order_field', 'crc')
    time_begin, time_end = getDateRange(-2)    # 默认-2
    time_range = (time_begin, time_end)
    porterror_query = __queryline(order_field)
    porterror_all_list = PortErrorDiff.objects.raw(
        porterror_query, (time_begin, time_end, time_begin, time_end)
    )
    page_of_objects, page_range = pages(request, porterror_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(
        time_range[0], '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(
        time_range[1], '%Y-%m-%d+%H:%M:%S')
    context['order_field'] = order_field
    context['porterror_search_form'] = PortErrorSearchForm()
    return render(request, 'port_error_list.html', context)


# 通过端口查找,端口下划分的ip及对应客户,最内层select可以与model对象再做一次join查询
__QUERY_ERROR_AFFECT = "\
    SELECT p_ip_tb.*, client_tb.group_id, client_tb.client_name, client_tb.ip \
    FROM (\
        SELECT pp_tb.*, ip_tb.device_ip \
        FROM (\
            SELECT id, device_name, `port`, logic_port \
            FROM cmdb.networkresource_ipmanresource \
            WHERE device_name = %s AND `port` = %s \
        ) AS pp_tb LEFT JOIN cmdb.networkresource_iprecord AS ip_tb \
        ON pp_tb.device_name = ip_tb.device_name AND pp_tb.logic_port = ip_tb.logic_port_num\
    ) AS p_ip_tb LEFT JOIN cmdb.networkresource_zxclientinfo AS client_tb \
    ON p_ip_tb.device_ip = client_tb.ip\
"


def ajax_search_error_effect(request):
    data = {}
    try:
        device_name = request.GET.get('device_name')
        port = request.GET.get('port')
        effect_list = PortErrorDiff.objects.raw(__QUERY_ERROR_AFFECT, (device_name, port))
        effect_dict = []
        i = 1
        for e in effect_list:
            effect_dict.append({'id': str(i), 'device_name': e.device_name,'port': e.port, 'group_id': str(e.group_id), 'client_name': str(e.client_name), 'ip': e.ip})
            i += 1
        data['status'] = 'success'
        data['effect_list'] = json.dumps(effect_dict)
        # data['effect_list'] = serializers.serialize("json", effect_list, fields=('device_name', 'port', 'logic_port', 'group_id', 'client_name')) # 多个联合查询的对象无法正确转换成json
        # print(data['effect_list'])
    except:
        data['status'] = 'error'
    return JsonResponse(data)


def search_port_error(request):
    context = {}
    order_field = request.GET.get('order_field', 'crc')
    porterror_search_form = PortErrorSearchForm(request.GET)
    if porterror_search_form.is_valid():
        time_begin = porterror_search_form.cleaned_data['time_begin']
        time_end = porterror_search_form.cleaned_data['time_end']
        porterror_query = __queryline(order_field)
        porterror_all_list = PortErrorDiff.objects.raw(
            porterror_query, (time_begin, time_end, time_begin, time_end)
        )
    else:
        context['porterror_search_form'] = porterror_search_form
        return render(request, 'port_error_list.html', context)

    page_of_objects, page_range = pages(request, porterror_all_list)

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(
        time_begin, '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(
        time_end, '%Y-%m-%d+%H:%M:%S')
    context['order_field'] = order_field
    context['porterror_search_form'] = porterror_search_form
    return render(request, 'port_error_list.html', context)


def export_porterror(request):
    time_begin = request.GET.get('time_begin', '')
    time_end = request.GET.get('time_end', '')
    if time_begin == '' or time_end == '':
        today_time = timezone.datetime.now()
        time_end = timezone.datetime(
            year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
        time_begin = time_end + timezone.timedelta(days=-2)  # 默认下载当天的数据
    else:
        time_begin = timezone.datetime.strptime(
            time_begin, '%Y-%m-%d %H:%M:%S')
        time_end = timezone.datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
    porterror_query = __queryline('crc')
    porterror_all_list = PortErrorDiff.objects.raw(
        porterror_query, (time_begin, time_end, time_begin, time_end)
    )
    output = rawQueryExportXls(
        porterror_all_list.columns, porterror_all_list, 'record_time')
    response = FileResponse(
        open(output, 'rb'), as_attachment=True, filename="porterror_result.xls")
    return response


# 单通设备检查模块
def oneway_list(request):
    time_begin, time_end = getDateRange(-1)
    time_range = (time_begin, time_end)
    oneway_all_list = OneWayDevice.objects.filter(
        record_time__range=time_range)
    page_of_objects, page_range = pages(request, oneway_all_list)
    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(
        time_begin, '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(
        time_end, '%Y-%m-%d+%H:%M:%S')
    context['oneway_search_form'] = OneWaySearchForm()
    return render(request, 'oneway_list.html', context)


def search_oneway(request):
    context = {}
    oneway_search_form = OneWaySearchForm(request.GET)
    if oneway_search_form.is_valid():
        time_begin = oneway_search_form.cleaned_data['time_begin']
        time_end = oneway_search_form.cleaned_data['time_end']
        oneway_all_list = OneWayDevice.objects.filter(
            record_time__range=(time_begin, time_end))
    else:
        context['oneway_search_form'] = oneway_search_form
        return render(request, 'oneway_list.html', context)

    page_of_objects, page_range = pages(request, oneway_all_list)

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(
        time_begin, '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(
        time_end, '%Y-%m-%d+%H:%M:%S')
    context['oneway_search_form'] = oneway_search_form
    return render(request, 'oneway_list.html', context)


def export_oneway(request):
    time_begin = request.GET.get('time_begin', '')
    time_end = request.GET.get('time_end', '')
    if time_begin == '' or time_end == '':
        today_time = timezone.datetime.now()
        time_end = timezone.datetime(
            year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
        time_begin = time_end + timezone.timedelta(days=-1)  # 默认下载当天的数据
    else:
        time_begin = timezone.datetime.strptime(
            time_begin, '%Y-%m-%d %H:%M:%S')
        time_end = timezone.datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
    oneway_all_list = OneWayDevice.objects.filter(
        record_time__range=(time_begin, time_end))

    output = exportXls(OneWayDevice._meta.fields,
                       oneway_all_list, 'record_time')
    response = FileResponse(
        open(output, 'rb'), as_attachment=True, filename="oneway_result.xls")
    return response
