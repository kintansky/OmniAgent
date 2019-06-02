from django.shortcuts import render, redirect
from .models import OpticalMoudleDiff, PortErrorDiff, OneWayDevice, PortErrorFixRecord
from django.utils import timezone
from .forms import MoudleSearchForm, PortErrorSearchForm, OneWaySearchForm, PortErrorOperationForm
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
'''
__PORTERROR_QUERY = "\
    SELECT error_info.*, npp.* FROM (\
        SELECT np.*, ni.port_description, ni.port_status \
            FROM omni_agent.inspection_porterrordiff as np \
            LEFT JOIN omni_agent.networkresource_ipmanresource AS ni \
            ON np.device_name = ni.device_name AND np.port = ni.port \
            WHERE np.record_time between %s AND %s\
        ) AS error_info \
    LEFT JOIN (\
        SELECT device_name, `port`, tx_now_power, tx_high_warm, tx_low_warm, tx_state, rx_now_power, rx_high_warm, rx_low_warm, rx_state, utility_in, utility_out, record_time \
            FROM omni_agent.inspection_portperf \
            WHERE record_time BETWEEN %s AND %s\
        ) AS npp \
    ON error_info.device_name = npp.device_name AND error_info.port = npp.port \
    AND DATE_FORMAT(error_info.record_time, '%Y-%m-%d') = DATE_FORMAT(npp.record_time, '%Y-%m-%d') \
"
'''

__PORTERROR_QUERY = "\
    SELECT new_tb.*, fix_tb.worker, fix_tb.claim FROM (\
        SELECT error_info.*, npp.tx_now_power, npp.tx_high_warm, npp.tx_low_warm, npp.tx_state, npp.rx_now_power, npp.rx_high_warm, npp.rx_low_warm, npp.rx_state, npp.utility_in, npp.utility_out FROM (\
            SELECT np.*, ni.port_description, ni.port_status \
                FROM omni_agent.inspection_porterrordiff as np \
                LEFT JOIN omni_agent.networkresource_ipmanresource AS ni \
                ON np.device_name = ni.device_name AND np.port = ni.port \
                WHERE np.record_time BETWEEN %s AND %s\
            ) AS error_info \
        LEFT JOIN (\
            SELECT device_name, `port`, tx_now_power, tx_high_warm, tx_low_warm, tx_state, rx_now_power, rx_high_warm, rx_low_warm, rx_state, utility_in, utility_out, record_time \
                FROM omni_agent.inspection_portperf \
                WHERE record_time BETWEEN %s AND %s\
            ) AS npp \
        ON error_info.device_name = npp.device_name AND error_info.port = npp.port \
        AND DATE_FORMAT(error_info.record_time, '%Y-%m-%d') = DATE_FORMAT(npp.record_time, '%Y-%m-%d') \
    ) AS new_tb LEFT JOIN (SELECT * FROM omni_agent.inspection_porterrorfixrecord WHERE claim = 1) AS fix_tb \
    ON new_tb.device_name = fix_tb.device_name AND new_tb.port = fix_tb.port \
"
# 注意修改__queryline的排序字段


def __queryline(order_field):
    if order_field == 'crc':
        porterror_query = __PORTERROR_QUERY + 'ORDER BY -new_tb.stateCRC'
    elif order_field == 'head':
        porterror_query = __PORTERROR_QUERY + 'ORDER BY -new_tb.stateIpv4HeadError'
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
            FROM omni_agent.networkresource_ipmanresource \
            WHERE device_name = %s AND `port` = %s \
        ) AS pp_tb LEFT JOIN omni_agent.networkresource_iprecord AS ip_tb \
        ON pp_tb.device_name = ip_tb.device_name AND pp_tb.logic_port = ip_tb.logic_port_num\
    ) AS p_ip_tb LEFT JOIN omni_agent.networkresource_zxclientinfo AS client_tb \
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


def ajax_port_operation_list(request):
    data = {}
    rid = request.GET.get('rid')
    target = PortErrorDiff.objects.get(id=int(rid))
    # 过往处理记录（最近10条）
    operation_old_records = PortErrorFixRecord.objects.filter(device_name=target.device_name, port=target.port, status=True).order_by('-begin_time')[0:10]
    data = portErrorEverOperationHtmlCallBack(operation_old_records, data)
    # 当前在处理的记录，如果能找到正在处理的记录，说明正在被处理
    try:
        operation_now_record = PortErrorFixRecord.objects.get(device_name=target.device_name, port=target.port, status=False)
        data['operating'] = 'yes'
        data['worker'] = operation_now_record.worker
        
        data = portOperationHtmlCallBack(data, rid)
        data['status'] = 'success'
        
    except Exception as err: # 如果没找到说明没有在处理的记录，需要先认领，再处理
        print(err)
        data['operating'] = 'no'
        data['operation_form'] = ''
        data['status'] = 'success'
    return JsonResponse(data)


def portErrorEverOperationHtmlCallBack(records, data):
    problem_dict = {'power': '光功率问题', 'moudle': '光模块故障', 'fiber': '尾纤问题', 'wdm': '波分故障', 'oth': '其他故障'}
    h = ''
    for r in records:
        begin = r.begin_time.strftime('%Y-%m-%d')
        end = r.end_time.strftime('%Y-%m-%d')
        h += '<li class="list-group-item list-group-item-success">' + \
                begin + ' 发现 ' + '<strong>' + problem_dict[r.problem_type] + '</strong>' + ' ' + end + ' 完成处理 处理人: ' + r.worker + \
            '</li>'
    data['operation-record'] = h
    return data


def portOperationHtmlCallBack(data, rid):
    h = '<form class="modal_form" action="" method="POST" rid="{}">'.format(rid)
    operation_form = PortErrorOperationForm()
    for f in operation_form:
        h += '<div class="form-group"><label for="{}" class="control-label">{}</label>{}</div>'.format(
            f.id_for_label, f.label, f)
    h += '</form>'
    data['operation_form'] = h
    return data


def ajax_port_operate(request, operation_type):
    data = {}
    if operation_type == 'claim':
        rid = request.POST.get('rid')
        target = PortErrorDiff.objects.get(id=int(rid))
        try:
            # 可能已经存在正在处理的记录的情况，这种不不要再新建记录
            PortErrorFixRecord.objects.get(device_name=target.device_name, port=target.port, claim=True)
            data['status'] = 'success'
        except:
            # 不存在正在处理的记录的情况，新建记录
            fix_record = PortErrorFixRecord()
            fix_record.device_name = target.device_name
            fix_record.port = target.port
            fix_record.worker = request.user.first_name
            fix_record.claim = True
            fix_record.save()
            data['status'] = 'success'
    elif operation_type == 'finish':
        of = PortErrorOperationForm(request.POST)
        rid = request.POST.get('rid')
        target = PortErrorDiff.objects.get(id=int(rid))
        if target.fix_status is None:  # 避免一些没刷新的问题
            fix_record = PortErrorFixRecord.objects.get(device_name=target.device_name, port=target.port, status=False, claim=True)
            if of.is_valid():
                if request.user.first_name == fix_record.worker:
                    fix_record.problem_type = of.cleaned_data['problem_type']
                    fix_record.problem_detail = of.cleaned_data['problem_detail']
                    fix_record.end_time = timezone.datetime.now()
                    fix_record.status = True
                    fix_record.claim = False
                    fix_record.save()
                    data['status'] = 'success'
                    target.fix_status = True
                    # 避免空字符回填的问题
                    if target.nowCRC is None:
                        target.nowCRC = 0
                    if target.nowIpv4HeaderError is None:
                        target.nowIpv4HeaderError = 0
                    if target.everCRC is None:
                        target.everCRC = 0
                    if target.everIpv4HeaderError is None:
                        target.everIpv4HeaderError = 0
                    if target.stateCRC is None:
                        target.stateCRC = 0
                    if target.stateIpv4HeadError is None:
                        target.stateIpv4HeadError = 0
                    target.save()
                else:
                    data['status'] = 'error'
                    data['error_info'] = '你非认领用户，认领用户为{}'.format(fix_record.worker)
            else:
                data['status'] = 'error'
                error_info = ''
                errorDict = of.errors.as_data()
                for f in errorDict:
                        error_info += '填写错误字段{}: {}'.format(f, errorDict[f])
                data['error_info'] = error_info
    return JsonResponse(data)


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
