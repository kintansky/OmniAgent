from django.shortcuts import render, redirect
from .models import OpticalMoudleDiff, PortErrorDiff
from django.utils import timezone
from .forms import MoudleSearchForm, PortErrorSearchForm
from funcpack.funcs import pages, getDateRange, exportXls, rawQueryExportXls
from django.http import FileResponse


# Create your views here.
def moudle_list(request):
    # 默认展示前3天数据
    moudle_all_list = OpticalMoudleDiff.objects.filter(record_time__range=getDateRange(-3))
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
            moudle_all_list = OpticalMoudleDiff.objects.filter(device_name__icontains=device_name, status__contains=status, record_time__range=time_range)
        elif status != '':
            moudle_all_list = OpticalMoudleDiff.objects.filter(status=status, record_time__range=time_range)
        else:
            moudle_all_list = OpticalMoudleDiff.objects.filter(record_time__range=time_range)
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
    context['time_begin'] = timezone.datetime.strftime(time_range[0], '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(time_range[1], '%Y-%m-%d+%H:%M:%S')
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
        time_begin = timezone.datetime.strptime(time_begin, '%Y-%m-%d %H:%M:%S')
        time_end = timezone.datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
        time_range = (time_begin, time_end)
        print(time_range)
    if device_name == status == '':
        moudle_all_list = OpticalMoudleDiff.objects.filter(record_time__range=time_range)
    else:
        if device_name != '':   # device_name != '' status == ''
            moudle_all_list = OpticalMoudleDiff.objects.filter(device_name__icontains=device_name, record_time__range=time_range)
        elif status != '':  # device_name == '' status != ''
            moudle_all_list = OpticalMoudleDiff.objects.filter(status=status, record_time__range=time_range)
        else:
            moudle_all_list = OpticalMoudleDiff.objects.filter(record_time__range=time_range)
    output = exportXls(OpticalMoudleDiff._meta.fields, moudle_all_list, 'record_time')
    response = FileResponse(open(output, 'rb'), as_attachment=True, filename="moudle_result.xls") # 使用Fileresponse替代以上两行
    return response

# port error 采用rawquery做连接查询，取出其他关联信息 
PORTERROR_QUERY = 'SELECT np.*, \
                    ni.port_description, ni.port_status \
                    FROM networkresource_porterrordiff as np LEFT JOIN networkresource_ipmanresource AS ni \
                    ON np.device_name = ni.device_name AND np.port = ni.port'
# PORTERROR_QUERY2 用于请求CRC+光功率的信息
PORTERROR_QUERY2 = "\
    SELECT error_info.*, npp.* FROM (\
        SELECT np.*, ni.port_description, ni.port_status \
            FROM networkresource_porterrordiff as np \
            LEFT JOIN networkresource_ipmanresource AS ni \
            ON np.device_name = ni.device_name AND np.port = ni.port \
            WHERE np.record_time between %s AND %s\
        ) AS error_info \
    LEFT JOIN (\
        SELECT device_name, `port`, tx_now_power, tx_state, rx_now_power, rx_state \
            FROM cmdb.networkresource_portperf \
            WHERE record_time BETWEEN %s AND %s\
        ) AS npp \
    ON error_info.device_name = npp.device_name AND error_info.port = npp.port \
    ORDER BY -error_info.stateCRC \
    "
    
def port_error_list(request):
    time_begin, time_end = getDateRange(-2)
    time_range = (time_begin, time_end)
    porterror_all_list = PortErrorDiff.objects.raw(
        PORTERROR_QUERY2, (time_begin, time_end, time_begin, time_end)
    )
    # porterror_all_list = PortErrorDiff.objects.raw(PORTERROR_QUERY)
    page_of_objects, page_range = pages(request, porterror_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(time_range[0], '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(time_range[1], '%Y-%m-%d+%H:%M:%S')
    context['porterror_search_form'] = PortErrorSearchForm()
    return render(request, 'port_error_list.html', context)

def search_port_error(request):
    context = {}
    porterror_search_form = PortErrorSearchForm(request.GET)
    if porterror_search_form.is_valid():
        time_begin = porterror_search_form.cleaned_data['time_begin']
        time_end = porterror_search_form.cleaned_data['time_end']
        # time_range = (time_begin, time_end)
        # porterror_all_list = PortErrorDiff.objects.raw(
        #     PORTERROR_QUERY + ' WHERE np.record_time between %s and %s', time_range
        # )
        porterror_all_list = PortErrorDiff.objects.raw(
            PORTERROR_QUERY2, (time_begin, time_end, time_begin, time_end)
        )
    else:
        context['porterror_search_form'] = porterror_search_form
        return render(request, 'port_error_list.html', context)

    page_of_objects, page_range = pages(request, porterror_all_list)

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['time_begin'] = timezone.datetime.strftime(time_begin, '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = timezone.datetime.strftime(time_end, '%Y-%m-%d+%H:%M:%S')
    context['porterror_search_form'] = porterror_search_form
    return render(request, 'port_error_list.html', context)

def export_porterror(request):
    time_begin = request.GET.get('time_begin', '')
    time_end = request.GET.get('time_end', '')
    if time_begin == '' or time_end == '':
        today_time = timezone.datetime.now()
        time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
        time_begin = time_end + timezone.timedelta(days=-1)  # 默认下载当天的数据
    else:
        time_begin = timezone.datetime.strptime(time_begin, '%Y-%m-%d %H:%M:%S')
        time_end = timezone.datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
    time_range = (time_begin, time_end)
    # porterror_all_list = PortErrorDiff.objects.raw(
    #     PORTERROR_QUERY + ' WHERE np.record_time between %s and %s', time_range
    # )   # 返回的事RawQuerySet对象，原有的导出函数不适用
    porterror_all_list = PortErrorDiff.objects.raw(
        PORTERROR_QUERY2, (time_begin, time_end, time_begin, time_end)
    )
    output = rawQueryExportXls(porterror_all_list.columns, porterror_all_list, 'record_time')
    response = FileResponse(open(output, 'rb'), as_attachment=True, filename="porterror_result.xls")
    return response
