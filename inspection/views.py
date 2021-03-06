from django.shortcuts import render, redirect
from .models import OpticalMoudleDiff, PortErrorDiff, OneWayDevice, OneWayDeviceTag, PortErrorFixRecord, NatPoolUsage, LinkPingTest, LinkPingHourAggregate, LinkPingCostStepAggregate
from networkresource.models import ZxClientInfo
from django.utils import timezone
from .forms import MoudleSearchForm, PortErrorSearchForm, OneWaySearchForm, OneWayTagForm, PortErrorOperationForm, NatPoolSearchForm, GroupClientSearchForm, PortErrorFixRecordSearchForm
from funcpack.funcs import pages, getDateRange, exportXls, rawQueryExportXls, objectDataSerializerRaw
from django.http import FileResponse, JsonResponse
# from django.core import serializers
import json
from django.db.models import F, Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

# 光模块检查模块
# @permission_required('inspection.view_opticalmoudlediff', login_url='/login/')
@staff_member_required(redirect_field_name='from', login_url='login')
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
                       moudle_all_list, ('record_time',))
    response = FileResponse(open(output, 'rb'), as_attachment=True,
                            filename="moudle_result.xls")  # 使用Fileresponse替代以上两行
    return response


# 端口质量模块
# port error 采用rawquery做连接查询，取出其他关联信息 用于请求CRC+光功率的信息

__PORTERROR_QUERY = '''
    SELECT error_info.*, npp.* FROM (
        SELECT np.*, ni.port_description, ni.port_status 
            FROM omni_agent.OM_REP_port_error_diff as np 
            LEFT JOIN omni_agent.MR_REC_ipman_resource AS ni 
            ON np.device_name = ni.device_name AND np.port = ni.port 
            WHERE np.record_time between %s AND %s
        ) AS error_info 
    LEFT JOIN (
        SELECT device_name, `port`, tx_now_power, tx_high_warm, tx_low_warm, tx_state, rx_now_power, rx_high_warm, rx_low_warm, rx_state, utility_in, utility_out, record_time 
            FROM omni_agent.OM_REC_port_perf 
            WHERE record_time BETWEEN %s AND %s
        ) AS npp 
    ON error_info.device_name = npp.device_name AND error_info.port = npp.port 
    AND DATE_FORMAT(error_info.record_time, '%%Y-%%m-%%d') = DATE_FORMAT(npp.record_time, '%%Y-%%m-%%d') 
'''

CRC_FILTER = 60
IPV4HEADERROR_FILTER = 1000
__PORTERROR_QUERY = '''
    SELECT 
        ped.*,
        des.port_description, des.port_status,
        pef.problem_type, pef.problem_detail, pef.begin_time, pef.end_time, pef.worker, pef.status, pef.claim,
        pp.tx_now_power, pp.tx_high_warm, pp.tx_low_warm, pp.tx_state, pp.rx_now_power, pp.rx_high_warm, pp.rx_low_warm, pp.rx_state, pp.utility_in, pp.utility_out,
        error_cnt_tb.cnt
    FROM (
        SELECT * FROM omni_agent.OM_REP_port_error_diff 
        WHERE record_time BETWEEN %s AND %s AND (stateCRC >= {} OR stateIpv4HeadError >= {})
    ) AS ped 
    LEFT JOIN omni_agent.MR_REC_ipman_resource AS des
        ON ped.device_name = des.device_name AND ped.port = des.port
    LEFT JOIN (
        SELECT * FROM omni_agent.OM_REC_port_error_fix_record WHERE claim = 1
    ) AS pef 
        ON ped.device_name = pef.device_name AND ped.port = pef.port
    LEFT JOIN (
        SELECT * FROM omni_agent.OM_REC_port_perf 
        WHERE record_time BETWEEN %s AND %s
    ) AS pp
        ON ped.device_name = pp.device_name AND ped.port = pp.port AND DATE_FORMAT(ped.record_time, '%%Y-%%m-%%d') = DATE_FORMAT(pp.record_time, '%%Y-%%m-%%d')
    LEFT JOIN (
        SELECT cnt_tb.*, COUNT(*) AS cnt FROM (
            SELECT device_name, port FROM omni_agent.OM_REP_port_error_diff 
            WHERE (stateCRC >= {} or stateIpv4HeadError >= {}) and record_time between DATE_SUB(CURDATE(), INTERVAL 7 DAY) and CURDATE()) AS cnt_tb GROUP BY cnt_tb.device_name, cnt_tb.port
    ) AS error_cnt_tb
    ON ped.device_name = error_cnt_tb.device_name AND ped.port = error_cnt_tb.port 
'''.format(CRC_FILTER, IPV4HEADERROR_FILTER, CRC_FILTER, IPV4HEADERROR_FILTER)
# 注意修改__queryline的排序字段


def __queryline(order_field, otherCmd=''):
    if order_field == 'crc' or order_field == '':
        porterror_query = __PORTERROR_QUERY + otherCmd + 'ORDER BY -stateCRC, -stateIpv4HeadError'
    elif order_field == 'head':
        porterror_query = __PORTERROR_QUERY + otherCmd + 'ORDER BY -stateIpv4HeadError, -stateCRC'
    return porterror_query


# @permission_required('inspection.view_porterrordiff', login_url='/login/')
@staff_member_required(redirect_field_name='from', login_url='login')
def port_error_list(request):
    order_field = request.GET.get('order_field', 'crc')
    time_begin, time_end = getDateRange(-2)    # 默认-2
    time_range = (time_begin, time_end)
    porterror_query = __queryline(order_field)
    porterror_all_list = PortErrorDiff.objects.raw(
        porterror_query, (time_begin, time_end, time_begin, time_end)
    )
    page_of_objects, page_range = pages(request, porterror_all_list)
    my_tasks_cnt = 0
    if request.user.is_authenticated:
        my_tasks_cnt = PortErrorFixRecord.objects.filter(worker=request.user.first_name, status=False).count()

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(
        time_range[0], '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(
        time_range[1], '%Y-%m-%d+%H:%M:%S')
    context['order_field'] = order_field
    context['my_tasks_cnt'] = my_tasks_cnt
    context['porterror_search_form'] = PortErrorSearchForm()
    return render(request, 'port_error_list.html', context)


# 通过端口查找,端口下划分的ip及对应客户,最内层select可以与model对象再做一次join查询
__QUERY_ERROR_AFFECT = '''
    SELECT p_ip_tb.*, client_tb.product_id, client_tb.client_name, client_tb.ip 
    FROM ( 
        SELECT pp_tb.*, ip_tb.device_ip, ip_tb.ip_type 
        FROM ( 
            SELECT id, device_name, `port`, logic_port 
            FROM omni_agent.networkresource_ipmanresource 
            WHERE device_name = %s AND `port` = %s 
        ) AS pp_tb 
        LEFT JOIN omni_agent.networkresource_iprecord AS ip_tb 
        ON pp_tb.device_name = ip_tb.device_name AND pp_tb.logic_port = ip_tb.logic_port_num HAVING ip_tb.ip_type IN ('public_outer', 'public_inner') 
    ) AS p_ip_tb LEFT JOIN omni_agent.networkresource_zxclientinfo AS client_tb 
    ON p_ip_tb.device_ip = client_tb.ip HAVING client_name IS NOT NULL 
'''


def ajax_search_error_effect(request):
    data = {}
    try:
        device_name = request.GET.get('device_name')
        port = request.GET.get('port')
        effect_list = PortErrorDiff.objects.raw(__QUERY_ERROR_AFFECT, (device_name, port))
        effect_dict = []
        i = 1
        for e in effect_list:
            effect_dict.append({'id': str(i), 'device_name': e.device_name,'port': e.port, 'product_id': str(e.product_id), 'client_name': str(e.client_name), 'ip': e.device_ip})
            i += 1
        data['status'] = 'success'
        data['effect_list'] = json.dumps(effect_dict)
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
        pwr_problem = porterror_search_form.cleaned_data['pwr_problem']
        otherCmd = ''
        if pwr_problem:
            otherCmd += 'HAVING tx_state = 0 OR rx_state = 0 '
        porterror_query = __queryline(order_field, otherCmd=otherCmd)
        porterror_all_list = PortErrorDiff.objects.raw(
            porterror_query, (time_begin, time_end, time_begin, time_end)
        )
    else:
        context['porterror_search_form'] = porterror_search_form
        return render(request, 'port_error_list.html', context)

    page_of_objects, page_range = pages(request, porterror_all_list)
    my_tasks_cnt = 0
    if request.user.is_authenticated:
        my_tasks_cnt = PortErrorFixRecord.objects.filter(worker=request.user.first_name, status=False).count()

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(
        time_begin, '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(
        time_end, '%Y-%m-%d+%H:%M:%S')
    context['order_field'] = order_field
    context['my_tasks_cnt'] = my_tasks_cnt
    context['pwr_problem'] = pwr_problem
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
        porterror_all_list.columns, porterror_all_list, ('record_time',))
    response = FileResponse(
        open(output, 'rb'), as_attachment=True, filename="porterror_result.xls")
    return response


def ajax_port_operation_list(request, path_type):
    #TODO: 适应task里面的新状态
    data = {}
    rid = request.GET.get('rid')
    if path_type == 'task_list':
        target = PortErrorFixRecord.objects.get(id=int(rid))
    elif path_type == 'error_list':
        target = PortErrorDiff.objects.get(id=int(rid))
    else:
        data['status'] = 'error'
        data['error_info'] = '非法请求路径'
        return JsonResponse[data]
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
    problem_dict = {'power': '光功率问题', 'moudle': '光模块故障', 'fiber': '尾纤问题', 'wdm': '波分故障', 'other': '其他故障'}
    h = ''
    for r in records:
        begin = r.begin_time.strftime('%Y-%m-%d')
        end = r.end_time.strftime('%Y-%m-%d')
        h += '<li class="list-group-item list-group-item-info">' + \
                begin + ' 至 ' + end + ' 处理了 ' + '<strong>' + problem_dict[r.problem_type] + ': </strong>' + r.problem_detail+\
                '<span class="badge">' + r.worker + '</span>' \
            '</li>'
    data['operation-record'] = h
    return data


def portOperationHtmlCallBack(data, rid):   # 构造处理完成时需要填写的表单
    h = '<form class="modal_form" action="" method="POST" rid="{}">'.format(rid)
    operation_form = PortErrorOperationForm()
    for f in operation_form:
        h += '<div class="form-group"><label for="{}" class="control-label">{}</label>{}</div>'.format(
            f.id_for_label, f.label, f)
    h += '</form>'
    data['operation_form'] = h
    return data

@staff_member_required(redirect_field_name='from', login_url='login')
def porterror_fix_list(request):
    context = {}
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
    # fix_records = PortErrorFixRecord.objects.all().order_by('-begin_time')
    fix_records = PortErrorFixRecord.objects.exclude(problem_detail__icontains='系统自判').order_by('-begin_time')
    page_of_objects, page_range = pages(request, fix_records)

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(
        time_begin, '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(
        time_end, '%Y-%m-%d+%H:%M:%S')
    context['port_error_fix_record_search_form'] = PortErrorFixRecordSearchForm()
    return render(request, 'port_error_fix_record_list.html', context)


def search_porterror_fix(request):
    context = {}
    port_error_fix_record_search_form = PortErrorFixRecordSearchForm(request.GET)
    if port_error_fix_record_search_form.is_valid():
        time_begin = port_error_fix_record_search_form.cleaned_data['time_begin']
        time_end = port_error_fix_record_search_form.cleaned_data['time_end']
        fix_records = PortErrorFixRecord.objects.exclude(problem_detail__icontains='系统自判').filter(begin_time__range=(time_begin, time_end)).order_by('-begin_time')
    else:
        context['port_error_fix_record_search_form'] = PortErrorFixRecordSearchForm()
        return render(request, 'port_error_fix_record_list.html', context)

    page_of_objects, page_range = pages(request, fix_records)

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(
        time_begin, '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(
        time_end, '%Y-%m-%d+%H:%M:%S')
    context['port_error_fix_record_search_form'] = port_error_fix_record_search_form
    return render(request, 'port_error_fix_record_list.html', context)


def export_porterrorfix(request):
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
    fix_records = PortErrorFixRecord.objects.exclude(problem_detail__icontains='系统自判').filter(begin_time__range=(time_begin, time_end))
    output = exportXls(PortErrorFixRecord._meta.fields,
                       fix_records, ('begin_time', 'end_time'))
    response = FileResponse(
        open(output, 'rb'), as_attachment=True, filename="oneway_result.xls")
    return response


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
    elif 'finish' in operation_type:
        of = PortErrorOperationForm(request.POST)
        rid = request.POST.get('rid')
        if operation_type == 'finish_tasks':
            target = PortErrorFixRecord.objects.get(id=int(rid))
            fix_status = target.status
        else:
            target = PortErrorDiff.objects.get(id=int(rid))
            fix_status = target.fix_status
        if not fix_status:  # 避免一些没刷新的问题
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
                    PortErrorDiff.objects.filter(device_name=target.device_name, port=target.port, fix_status=False, record_time__lte=timezone.datetime.now()).update(fix_status=True)
                    # target.fix_status = True
                    # # 避免空字符回填的问题
                    # if target.nowCRC is None:
                    #     target.nowCRC = 0
                    # if target.nowIpv4HeaderError is None:
                    #     target.nowIpv4HeaderError = 0
                    # if target.everCRC is None:
                    #     target.everCRC = 0
                    # if target.everIpv4HeaderError is None:
                    #     target.everIpv4HeaderError = 0
                    # if target.stateCRC is None:
                    #     target.stateCRC = 0
                    # if target.stateIpv4HeadError is None:
                    #     target.stateIpv4HeadError = 0
                    # target.save()
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


__QUERY_MY_FIX_TASKS = '''
    SELECT 
        pef.id, pef.device_name, pef.port, pef.worker, pef.claim, pef.status, pef.begin_time,
        ped.stateCRC, ped.stateIpv4HeadError, ped.record_time, ped.fix_status,
        pp.tx_now_power, pp.tx_high_warm, pp.tx_low_warm, pp.tx_state, pp.rx_now_power, pp.rx_high_warm, pp.rx_low_warm, pp.rx_state, pp.utility_in, pp.utility_out 
    FROM (
        SELECT * FROM OM_REC_port_error_fix_record WHERE worker = %s 
    ) AS pef 
    left JOIN (
        SELECT * FROM OM_REP_port_error_diff 
        WHERE record_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND CURDATE()
    ) AS ped
    ON pef.device_name = ped.device_name AND pef.port = ped.port 
    LEFT JOIN OM_REC_port_perf AS pp
    ON pef.device_name = pp.device_name AND pef.port = pp.port AND DATE_FORMAT(ped.record_time, '%%Y-%%m-%%d') = DATE_FORMAT(pp.record_time, '%%Y-%%m-%%d')
    ORDER BY begin_time DESC, fix_status
'''

@staff_member_required(redirect_field_name='from', login_url='login')
def my_port_error_tasks(request):
    context = {}
    worker = request.user.first_name
    porterror_query = __QUERY_MY_FIX_TASKS
    porterror_all_list = PortErrorDiff.objects.raw(
        porterror_query, (worker,)
    )
    page_of_objects, page_range = pages(request, porterror_all_list)
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    return render(request, 'my_port_error_tasks.html', context)



# 单通设备检查模块
__QUERY_ONEWAY_LIST = '''
    SELECT 
        dev.*,
        tag.delay_count, tag.tag, tag.tag_user, tag.tag_time, 
        DATE_ADD(tag_time, INTERVAL delay_count DAY) AS end_time, 
        (DATE_SUB(tag_time, INTERVAL 1 day) < record_time AND record_time < DATE_ADD(tag_time, INTERVAL delay_count day) ) AS not_show 
    FROM ( 
        SELECT * FROM omni_agent.OM_REP_oneway_device WHERE record_time BETWEEN %s AND %s 
    )AS dev 
    LEFT JOIN omni_agent.OM_REC_oneway_device_tag AS tag 
    ON dev.device_name = tag.device_name AND dev.port = tag.port 
'''
__ONEWAY_ORDER_FIELD = 'ORDER BY not_show ASC, record_time DESC'


# @permission_required('inspection.view_onewaydevice', login_url='/login/')
@staff_member_required(redirect_field_name='from', login_url='login')
def oneway_list(request):
    time_begin, time_end = getDateRange(-1)
    time_range = (time_begin, time_end)
    oneway_all_list = OneWayDevice.objects.raw(__QUERY_ONEWAY_LIST+__ONEWAY_ORDER_FIELD, time_range)
    page_of_objects, page_range = pages(request, oneway_all_list)
    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    # context['time_begin'] = timezone.datetime.strftime(time_begin, '%Y-%m-%d+%H:%M:%S')
    # context['time_end'] = timezone.datetime.strftime(time_end, '%Y-%m-%d+%H:%M:%S')
    context['search_paras'] = 'time_begin={}&time_end={}&device_name={}'.format(timezone.datetime.strftime(time_begin, '%Y-%m-%d+%H:%M:%S'), timezone.datetime.strftime(time_end, '%Y-%m-%d+%H:%M:%S'), '')
    context['oneway_search_form'] = OneWaySearchForm()
    context['oneway_tag_form'] = OneWayTagForm()
    return render(request, 'oneway_list.html', context)


def search_oneway(request):
    context = {}
    oneway_search_form = OneWaySearchForm(request.GET)
    if oneway_search_form.is_valid():
        time_begin = oneway_search_form.cleaned_data['time_begin']
        time_end = oneway_search_form.cleaned_data['time_end']
        device_name = oneway_search_form.cleaned_data['device_name']
        device_filter = ''
        if device_name != '' or device_name is not None:
            device_filter = "HAVING device_name like '%{}%' ".format(device_name)
        oneway_all_list = OneWayDevice.objects.raw(__QUERY_ONEWAY_LIST+device_filter+__ONEWAY_ORDER_FIELD, (time_begin, time_end))
    else:
        context['oneway_search_form'] = oneway_search_form
        context['oneway_tag_form'] = OneWayTagForm()
        return render(request, 'oneway_list.html', context)

    page_of_objects, page_range = pages(request, oneway_all_list)

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['search_paras'] = 'time_begin={}&time_end={}&device_name={}'.format(timezone.datetime.strftime(time_begin, '%Y-%m-%d+%H:%M:%S'), timezone.datetime.strftime(time_end, '%Y-%m-%d+%H:%M:%S'), device_name)
    context['oneway_search_form'] = oneway_search_form
    context['oneway_tag_form'] = OneWayTagForm()
    return render(request, 'oneway_list.html', context)


def tag_oneway_device(request):
    data = {}
    rid = request.POST.get('rid')
    delay_tag = request.POST.get('delay_tag')
    delay_days = request.POST.get('delay_days')
    target = OneWayDevice.objects.get(id=int(rid))
    try:
        oneway_tag = OneWayDeviceTag.objects.get(device_name=target.device_name, port=target.port)
        oneway_tag.delay_count = int(delay_days)
        oneway_tag.tag = delay_tag
        oneway_tag.tag_user = request.user.first_name
        oneway_tag.tag_time = timezone.datetime.now()
        oneway_tag.save()
    except ObjectDoesNotExist:
        oneway_tag = OneWayDeviceTag()
        oneway_tag.device_name = target.device_name
        oneway_tag.port = target.port
        oneway_tag.delay_count = int(delay_days)
        oneway_tag.tag = delay_tag
        oneway_tag.tag_user = request.user.first_name
        oneway_tag.tag_time = timezone.datetime.now()
        oneway_tag.save()
    data['status'] = 'success'
    return JsonResponse(data)


def cancle_tag_oneway(request):
    data = {}
    rid = request.POST.get('rid')
    target = OneWayDevice.objects.get(id=int(rid))
    try:
        oneway_tag = OneWayDeviceTag.objects.get(device_name=target.device_name, port=target.port)
        oneway_tag.delete()
    except ObjectDoesNotExist:
        pass
    data['status'] = 'success'
    return JsonResponse(data)


def export_oneway(request):
    time_begin = request.GET.get('time_begin', '')
    time_end = request.GET.get('time_end', '')
    device_name = request.GET.get('device_name', '')
    if time_begin == '' or time_end == '':
        today_time = timezone.datetime.now()
        time_end = timezone.datetime(
            year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
        time_begin = time_end + timezone.timedelta(days=-1)  # 默认下载当天的数据
    else:
        time_begin = timezone.datetime.strptime(
            time_begin, '%Y-%m-%d %H:%M:%S')
        time_end = timezone.datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
    if device_name != '':
        oneway_all_list = OneWayDevice.objects.filter(device_name__icontains=device_name, record_time__range=(time_begin, time_end))
    else:
        oneway_all_list = OneWayDevice.objects.filter(record_time__range=(time_begin, time_end))

    output = exportXls(OneWayDevice._meta.fields,
                       oneway_all_list, ('record_time',))
    response = FileResponse(
        open(output, 'rb'), as_attachment=True, filename="oneway_result.xls")
    return response


__GROUP_CLIENT_QUERY = '''
    SELECT client_info.*, re_tb.port_phy_status, re_tb.port_status FROM ( 
        SELECT 
            zx_tb.id, zx_tb.client_name, zx_tb.product_id, zx_tb.ip, zx_tb.guard_level, 
            ip_tb.device_name, ip_tb.logic_port, ip_tb.logic_port_num, ip_tb.ip_description 
        FROM omni_agent.MR_REC_group_client_info as zx_tb 
        LEFT JOIN omni_agent.MR_REC_ip_record AS ip_tb 
        ON zx_tb.ip = ip_tb.device_ip HAVING zx_tb.ip != '' 
    ) AS client_info 
    LEFT JOIN omni_agent.MR_REC_ipman_resource AS re_tb 
    ON client_info.device_name = re_tb.device_name AND client_info.logic_port_num = re_tb.logic_port 
'''


# @permission_required('networkresource.view_zxclientinfo', login_url='/login/')
@staff_member_required(redirect_field_name='from', login_url='login')
def group_client_list(request):
    context = {}
    group_client_all_list = ZxClientInfo.objects.raw(__GROUP_CLIENT_QUERY)
    page_of_objects, page_range = pages(request, group_client_all_list)

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['group_client_search_form'] = GroupClientSearchForm()
    return render(request, 'group_client_list.html', context)


def search_group_client(request):
    context = {}
    group_client_search_form = GroupClientSearchForm(request.GET)
    if group_client_search_form.is_valid():
        client_name = group_client_search_form.cleaned_data['client_name']
        product_id = group_client_search_form.cleaned_data['product_id']
        if client_name != '' and product_id is None:
            group_client_all_list = ZxClientInfo.objects.raw(__GROUP_CLIENT_QUERY+"HAVING client_info.client_name like '%{}%'".format(client_name))
        elif client_name == '' and product_id is not None:
            group_client_all_list = ZxClientInfo.objects.raw(__GROUP_CLIENT_QUERY+"HAVING client_info.product_id = {}".format(product_id))
        elif client_name != '' and product_id is not None:
            group_client_all_list = ZxClientInfo.objects.raw(__GROUP_CLIENT_QUERY+"HAVING client_info.client_name like '%{}%' and client_info.product_id = {}".format(client_name, product_id))
        else:
            group_client_all_list = ZxClientInfo.objects.raw(__GROUP_CLIENT_QUERY)
    else:
        context['group_client_search_form'] = group_client_search_form
        return render(request, 'group_client_list.html', context)
    page_of_objects, page_range = pages(request, group_client_all_list)
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['group_client_search_form'] = group_client_search_form
    return render(request, 'group_client_list.html', context)


# @permission_required('inspection.view_natpoolusage', login_url='/login/')
@staff_member_required(redirect_field_name='from', login_url='login')
def natpool_list(request):
    context = {}
    natpool_all_list = NatPoolUsage.objects.filter(record_time__range=getDateRange(-2)).annotate(nat_total=(F('device1_nat_usage')+F('device2_nat_usage'))).order_by(F('nat_total').desc())
    page_of_objects, page_range = pages(request, natpool_all_list)
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['natpool_search_form'] = NatPoolSearchForm()
    return render(request, 'natpool.html', context)


def search_natpool(request):
    context = {}
    natpool_search_form = NatPoolSearchForm(request.GET)
    if natpool_search_form.is_valid():
        time_begin = natpool_search_form.cleaned_data['time_begin']
        time_end = natpool_search_form.cleaned_data['time_end']
        device_name = natpool_search_form.cleaned_data['device_name']
        if device_name != '':
            natpool_all_list = NatPoolUsage.objects.filter(Q(device1__icontains=device_name) | Q(device2__icontains=device_name), Q(record_time__range=(time_begin, time_end))).annotate(nat_total=(F('device1_nat_usage')+F('device2_nat_usage'))).order_by(F('nat_total').desc())
            context['search_device_name'] = device_name
        else:
            natpool_all_list = NatPoolUsage.objects.filter(record_time__range=(time_begin, time_end)).annotate(nat_total=(F('device1_nat_usage')+F('device2_nat_usage'))).order_by(F('nat_total').desc())
    else:
        context['natpool_search_form'] = natpool_search_form
        return render(request, 'natpool.html', context)

    page_of_objects, page_range = pages(request, natpool_all_list)

    context['records'] = page_of_objects
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(time_begin, '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(time_end, '%Y-%m-%d+%H:%M:%S')
    context['natpool_search_form'] = natpool_search_form
    return render(request, 'natpool.html', context)


__NATPOOL_QUERY = '''
    SELECT id, device1, device1_nat_usage, device2, device2_nat_usage, record_time, (device1_nat_usage + device2_nat_usage) AS nat_total 
    FROM OM_REC_nat_pool_usage 
    WHERE (device1 LIKE '%%{}%%' OR device2 LIKE '%%{}%%') AND record_time BETWEEN '{}' and '{}' 
    ORDER BY (device1_nat_usage + device2_nat_usage) DESC 
'''

def export_natpool(request):
    time_begin = request.GET.get('time_begin', '')
    time_end = request.GET.get('time_end', '')
    device_name = request.GET.get('device_name', '')
    if time_begin == '' or time_end == '':
        today_time = timezone.datetime.now()
        time_end = timezone.datetime(
            year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
        time_begin = time_end + timezone.timedelta(days=-1)  # 默认下载当天的数据
    else:
        time_begin = timezone.datetime.strptime(
            time_begin, '%Y-%m-%d %H:%M:%S')
        time_end = timezone.datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
    # 因为有一个自定义字段的原因，直接query取不到自定义字段名，因此使用raw，以便使用函数导出
    natpool_all_list = NatPoolUsage.objects.raw(__NATPOOL_QUERY.format(device_name, device_name, time_begin, time_end))
    
    output = rawQueryExportXls(natpool_all_list.columns, natpool_all_list, ('record_time',))
    response = FileResponse(
        open(output, 'rb'), as_attachment=True, filename="natpool_usage.xls")
    return response


__PING_QUERY = '''
    SELECT 
    id, source_device, target_device, 
    CAST(round(AVG(loss), 0) AS SIGNED) AS avg_loss, CAST(round(AVG(cost), 0) AS SIGNED) AS avg_cost, 
    CAST(SUM(high_loss) AS SIGNED) AS high_loss_cnt, CAST(SUM(high_cost) AS SIGNED) AS high_cost_cnt FROM (
    SELECT *,
    if(loss>0, 1, 0) AS high_loss,
    case 
        when target_device LIKE '%%IPMAN-RT%%' AND cost > 10 then 1
        when target_device LIKE '%%IPMAN-SW%%' AND cost > 10 then 1
        when source_device LIKE '%%IPMAN-BNG%%' AND (target_device LIKE '%%OLT%%' OR target_device LIKE '%%FH%%') AND cost > 10 then 1
        when target_device LIKE 'GDGZ-%%' AND cost > 20 then 1
        when (target_device LIKE '%%-OTV%%' OR target_device LIKE '%%CDN%%') AND cost > 20 then 1
        when source_device LIKE '%%IPMAN-SR%%' AND (target_device LIKE '%%OLT%%' OR target_device LIKE '%%FH%%') AND cost > 20 then 1
    ELSE 0
    END AS high_cost
    FROM OM_REP_ping_test WHERE loss != -1 AND record_time BETWEEN %s AND %s
    ) AS oneday
    GROUP BY source_device, target_device 
'''

def __queryline_ping(order_field, filterCmd=''):
    if order_field == 'loss':
        cmd = __PING_QUERY + filterCmd + ' ORDER BY avg_loss DESC, high_loss_cnt DESC, avg_cost DESC, high_cost_cnt DESC'
    if order_field == 'cost':
        cmd = __PING_QUERY + filterCmd + ' ORDER BY avg_cost DESC, high_cost_cnt DESC, avg_loss DESC, high_loss_cnt DESC'
    return cmd
# 过滤条件
__PING_FILTER_HIGH_COST_CNT = 5
__PING_FILTER_HIGH_LOSS_CNT = 5


# @permission_required('inspection.view_linkpingtest', login_url='/login/')
@staff_member_required(redirect_field_name='from', login_url='login')
def ping_result_list(request):
    context = {}
    time_begin, _ = getDateRange(-2)
    time_end, _ = getDateRange(-1)
    time_range = (time_begin, time_end)
    cost_group_list = LinkPingCostStepAggregate.objects.all().order_by('id')
    cost_hour_group_list = LinkPingHourAggregate.objects.all().order_by('id')
    l = {}
    for cost_hour in cost_hour_group_list:
        temp = []
        for f in cost_hour._meta.fields[2::]:
            val = cost_hour.serializable_value(f.attname)
            temp.append(str(val))
        l[cost_hour.direction] = ','.join(temp)
    # print(l)
    ping_result_high_loss_list = LinkPingTest.objects.raw(
        __queryline_ping('loss', 'HAVING high_loss_cnt > {}'.format(__PING_FILTER_HIGH_LOSS_CNT)),
        time_range
    )
    ping_result_high_cost_list = LinkPingTest.objects.raw(
        __queryline_ping('cost', 'HAVING high_cost_cnt > {}'.format(__PING_FILTER_HIGH_LOSS_CNT)),
        time_range
    )
    context['cost_group_list'] = cost_group_list
    context['cost_hour_group_list'] = l
    context['high_loss_list'] = ping_result_high_loss_list
    context['high_cost_list'] = ping_result_high_cost_list
    return render(request, 'ping_result.html', context)


def ping_result_detail(request):
    context = {}
    source_device = request.GET.get('source_device', '')
    target_device = request.GET.get('target_device', '')
    target_ip = request.GET.get('target_ip', '')
    time_begin, _ = getDateRange(-2)
    time_end, _ = getDateRange(-1)
    ping_detail_list = LinkPingTest.objects.filter(
        source_device=source_device, target_device=target_device, 
        record_time__range=(time_begin, time_end)
    ).order_by('-record_time')
    page_of_objects, page_range = pages(request, ping_detail_list)
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['search_paras'] = '&source_device={}&target_device={}'.format(source_device, target_device)
    return render(request, 'ping_result_detail.html', context)