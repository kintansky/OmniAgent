from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Device, DeviceManufactor
from .forms import AddDeviceForm
from django.conf import settings

# Create your views here.
def device_list(request):
    device_all_list = Device.objects.all()
    paginator = Paginator(device_all_list, settings.EACH_PAGE_DEVICES_NUMBER)
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
        device_all_list = Device.objects.filter(device_name__icontains=device_name)
    elif ip_address != '' and device_name != '':
        device_all_list = Device.objects.filter(device_name__icontains=device_name, device_ip=ip_address)
    else:
        device_all_list = Device.objects.all()

    paginator = Paginator(device_all_list, settings.EACH_PAGE_DEVICES_NUMBER)
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
            NewDevice.device_manufactor = get_object_or_404(DeviceManufactor, manufactor_name=dm)
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
