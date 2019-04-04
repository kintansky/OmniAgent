from django.shortcuts import render, redirect
from .models import OpticalMoudleDiff, PortErrorDiff
import datetime
from django.utils import timezone
from .forms import MoudleSearchForm, PortErrorSearchForm
from funcpack.funcs import pages, exportXls
from django.http import FileResponse

def getDateRange(days):
    today_time = timezone.datetime.now()
    time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
    time_begin = time_end + timezone.timedelta(days=days)  # 负数向前
    return time_begin, time_end

# Create your views here.
def moudle_list(request):
    # 获取当天00:00至第二天00:00
    # today_time = timezone.datetime.now()
    # time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
    # time_begin = time_end + timezone.timedelta(days=-3)  # 展示前3天数据
    moudle_all_list = OpticalMoudleDiff.objects.filter(record_time__range=getDateRange(-3))
    # moudle_all_list = OpticalMoudleDiff.objects.all()

    page_of_objects, page_range = pages(request, moudle_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['count'] = OpticalMoudleDiff.objects.all().count()
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
    context['time_begin'] = datetime.datetime.strftime(time_begin, '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = datetime.datetime.strftime(time_end, '%Y-%m-%d+%H:%M:%S')
    context['moudle_search_form'] = moudle_search_form
    
    return render(request, 'moudle_list.html', context)

def export_moudle(request):
    device_name = request.GET.get('device_name', '')
    status = request.GET.get('status', '')
    time_begin = request.GET.get('time_begin', '')
    time_end = request.GET.get('time_end', '')
    if time_begin == '' or time_end == '':
        today_time = timezone.datetime.now()
        time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
        time_begin = time_end + timezone.timedelta(days=-1)  # 默认下载前一天的数据
    else:
        time_begin = datetime.datetime.strptime(time_begin, '%Y-%m-%d+%H:%M:%S')
        time_end = datetime.datetime.strptime(time_end, '%Y-%m-%d+%H:%M:%S')
    time_range = (time_begin, time_end)
    if device_name == status == '':
        moudle_all_list = OpticalMoudleDiff.objects.filter(record_time__range=time_range)
    else:
        if device_name != '':
            moudle_all_list = OpticalMoudleDiff.objects.filter(device_name__icontains=device_name, status__contains=status, record_time__range=time_range)
        elif status != '':
            moudle_all_list = OpticalMoudleDiff.objects.filter(status=status, record_time__range=time_range)
        else:
            moudle_all_list = OpticalMoudleDiff.objects.filter(record_time__range=time_range)
    output = exportXls(OpticalMoudleDiff._meta.fields, moudle_all_list)
    response = FileResponse(open(output, 'rb'), as_attachment=True, filename="moudle_result.xls") # 使用Fileresponse替代以上两行
    return response


def port_error_list(request):
    # 获取当天00:00至第二天00:00
    porterror_all_list = PortErrorDiff.objects.filter(record_time__range=getDateRange(-2))
    page_of_objects, page_range = pages(request, porterror_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['count'] = PortErrorDiff.objects.all().count()
    context['porterror_search_form'] = PortErrorSearchForm()
    return render(request, 'port_error_list.html', context)

def search_port_error(request):
    porterror_search_form = PortErrorSearchForm(request.GET)
    if porterror_search_form.is_valid():
        device_name = porterror_search_form.cleaned_data['device_name']
        time_begin = porterror_search_form.cleaned_data['time_begin']
        time_end = porterror_search_form.cleaned_data['time_end']
        time_range = (time_begin, time_end)
        if device_name != '':
            porterror_all_list = PortErrorDiff.objects.filter(record_time__range=time_range)
        else:
            porterror_all_list = PortErrorDiff.objects.filter(device_name=device_name, record_time__range=time_range)
    else:
        context = {}
        context['porterror_search_form'] = porterror_search_form
        return render(request, 'port_error_list.html', context)

    page_of_objects, page_range = pages(request, porterror_all_list)

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['search_device_name'] = device_name
    context['time_begin'] = datetime.datetime.strftime(time_begin, '%Y-%m-%d+%H:%M:%S')
    context['time_end'] = datetime.datetime.strftime(time_end, '%Y-%m-%d+%H:%M:%S')
    context['porterror_search_form'] = porterror_search_form
    return render(request, 'port_error_list.html', context)

def export_porterror(request):
    device_name = request.GET.get('device_name', '')
    time_begin = request.GET.get('time_begin', '')
    time_end = request.GET.get('time_end', '')
    if time_begin == '' or time_end == '':
        today_time = timezone.datetime.now()
        time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
        time_begin = time_end + timezone.timedelta(days=-1)  # 默认下载当天的数据
    else:
        time_begin = datetime.datetime.strptime(time_begin, '%Y-%m-%d+%H:%M:%S')
        time_end = datetime.datetime.strptime(time_end, '%Y-%m-%d+%H:%M:%S')
    time_range = (time_begin, time_end)
    if device_name == '':
        porterror_all_list = PortErrorDiff.objects.filter(record_time__range=time_range)
    else:
        porterror_all_list = PortErrorDiff.objects.filter(device_name__icontains=device_name, record_time__range=time_range)
    output = exportXls(PortErrorDiff._meta.fields, porterror_all_list)
    response = FileResponse(open(output, 'rb'), as_attachment=True, filename="porterror_result.xls")
    return response
