from django.shortcuts import render
from .models import PublicIpRecord
from django.core.paginator import Paginator
from django.conf import settings
from .forms import IPsearchForm

# Create your views here.
def ip_list(request):
    ip_all_list = PublicIpRecord.objects.all()

    paginator = Paginator(ip_all_list, settings.EACH_PAGE_DEVICES_NUMBER)
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
    context['count'] = PublicIpRecord.objects.all().count()
    context['ip_search_form'] = IPsearchForm()
    return render(request, 'iprecord.html', context)

def search_ip(request):
    ip_search_form = IPsearchForm(request.GET)
    if ip_search_form.is_valid():
        ip_address = ip_search_form.cleaned_data['ip_address']
        device_name = ip_search_form.cleaned_data['device_name']
        ip_description = ip_search_form.cleaned_data['description']
        if ip_address != '' and device_name == '':
            ip_all_list = PublicIpRecord.objects.filter(device_ip=ip_address, ip_description__icontains=ip_description)
        elif device_name != '' and ip_address == '':
            ip_all_list = PublicIpRecord.objects.filter(device_name=device_name, ip_description__icontains=ip_description)
        elif device_name != '' and ip_address != '':
            ip_all_list = PublicIpRecord.objects.filter(device_name=device_name, device_ip=ip_address, ip_description__icontains=ip_description)
        else:
            ip_all_list = PublicIpRecord.objects.filter(ip_description__icontains=ip_description)

    paginator = Paginator(ip_all_list, settings.EACH_PAGE_DEVICES_NUMBER)
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
    context['count'] = PublicIpRecord.objects.all().count()
    context['search_ip_address'] = ip_address
    context['search_device_name'] = device_name
    context['search_description'] = ip_description
    context['ip_search_form'] = ip_search_form
    return render(request, 'iprecord.html', context)
