from django.shortcuts import render, redirect
from .models import OpticalMoudleDiff
from django.core.paginator import Paginator
from django.conf import settings
import datetime
from django.utils import timezone
import pytz
from .forms import MoudleSearchForm

TODAY_TIME = timezone.datetime.now()
TZ = pytz.timezone(timezone.get_current_timezone_name())

# Create your views here.
def moudle_list(request):
    # 获取当天00:00至第二天00:00
    time_end = timezone.datetime(year=TODAY_TIME.year, month=TODAY_TIME.month, day=TODAY_TIME.day, hour=23, minute=59, second=59)
    time_end = TZ.localize(time_end)    # pytz和django的timezone获取的Shanghai时间与北京时间差6分钟，通过这样才能修正，否则转换为UTC后匹配有问题
    time_begin = time_end + timezone.timedelta(days=-5)  # 展示前3天数据
    moudle_all_list = OpticalMoudleDiff.objects.filter(record_time__range=(time_begin, time_end))
    # moudle_all_list = OpticalMoudleDiff.objects.all()

    paginator = Paginator(moudle_all_list, settings.EACH_PAGE_DEVICES_NUMBER)
    page_num = request.GET.get('page', 1)
    page_of_objects = paginator.get_page(page_num)
    current_page_num = page_of_objects.number
    page_range = list(range(max(current_page_num-2, 1), min(current_page_num+3, paginator.num_pages)+1))
    if page_range[0] - 1 > 2:
        page_range.insert(0, '...')
    if paginator.num_pages-page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    
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

    paginator = Paginator(moudle_all_list, settings.EACH_PAGE_DEVICES_NUMBER)
    page_num = request.GET.get('page', 1)
    page_of_objects = paginator.get_page(page_num)
    current_page_num = page_of_objects.number
    page_range = list(range(max(current_page_num-2, 1), min(current_page_num+3, paginator.num_pages)+1))
    if page_range[0] - 1 > 2:
        page_range.insert(0, '...')
    if paginator.num_pages-page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

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
