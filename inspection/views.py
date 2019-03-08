from django.shortcuts import render, redirect
from .models import OpticalMoudleDiff
import datetime
from django.utils import timezone
from .forms import MoudleSearchForm
import sys
from os.path import abspath, join, dirname
sys.path.insert(0, join(abspath(dirname('omni')), 'funcpack'))
from funcpack.funcs import pages

# Create your views here.
def moudle_list(request):
    # 获取当天00:00至第二天00:00
    today_time = timezone.datetime.now()
    time_end = timezone.datetime(year=today_time.year, month=today_time.month, day=today_time.day, hour=23, minute=59, second=59)
    time_begin = time_end + timezone.timedelta(days=-3)  # 展示前3天数据
    moudle_all_list = OpticalMoudleDiff.objects.filter(record_time__range=(time_begin, time_end))
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
