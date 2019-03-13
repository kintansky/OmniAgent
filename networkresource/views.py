from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import IpmanResource, IpRecord, PublicIpAllocation
from .forms import IPsearchForm, PortSearchForm, IpAllocateForm
from funcpack.funcs import pages, exportXls
from django.http import FileResponse

# Create your views here.
# port views
def show_ports(request):
    context = {}
    context['port_search_form'] = PortSearchForm()
    return render(request, 'resource.html', context)

def search_device_ports(request):
    port_search_form = PortSearchForm(request.GET)
    if port_search_form.is_valid():
        device_name = port_search_form.cleaned_data['device_name']
        slot = port_search_form.cleaned_data['slot']
        port = port_search_form.cleaned_data['port']
        port_description = port_search_form.cleaned_data['port_description']
        if port != '':
            target_ports = IpmanResource.objects.filter(device_name=device_name, port=port, port_description__icontains=port_description)    # 有明确端口的只返回一条
            target_slot = target_ports.values_list('slot')
        elif slot is not None:    # 没有明确端口，有明确的板卡信息，搜索整板卡
            target_ports = IpmanResource.objects.filter(device_name=device_name, slot=slot, port_description__icontains=port_description)
            target_slot = target_ports.values_list('slot')
        elif port_description != '':    # 端口、板卡均不指定，只指定描述
            target_ports = IpmanResource.objects.filter(device_name=device_name, port_description__icontains=port_description)
            target_slot = target_ports.values_list('slot')
    else:
        context = {}
        context['port_search_form'] = port_search_form
        return render(request, 'resource.html', context)
        
    context = {}
    context['device_name'] = device_name
    context['target_slot'] = target_slot
    context['target_ports'] = target_ports
    context['port_search_form'] = port_search_form
    return render(request, 'resource.html', context)


# iprecord views
def ip_list(request):
    ip_all_list = IpRecord.objects.all()
    page_of_objects, page_range = pages(request, ip_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['count'] = IpRecord.objects.all().count()
    context['ip_search_form'] = IPsearchForm()
    return render(request, 'iprecord.html', context)

def search_ip(request):
    ip_search_form = IPsearchForm(request.GET)
    if ip_search_form.is_valid():
        ip_address = ip_search_form.cleaned_data['ip_address']
        device_name = ip_search_form.cleaned_data['device_name']
        ip_description = ip_search_form.cleaned_data['description']
        if ip_address != '':
            ip_all_list = IpRecord.objects.filter(device_ip=ip_address)
        elif device_name != '':
            ip_all_list = IpRecord.objects.filter(device_name=device_name, ip_description__icontains=ip_description)
        elif ip_description != '':
            ip_all_list = IpRecord.objects.filter(ip_description__icontains=ip_description)
        else:
            ip_all_list = IpRecord.objects.all()
    else:
        context = {}
        context['ip_search_form'] = ip_search_form
        return render(request, 'iprecord.html', context)

    page_of_objects, page_range = pages(request, ip_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['count'] = IpRecord.objects.all().count()
    context['search_ip_address'] = ip_address
    context['search_device_name'] = device_name
    context['search_description'] = ip_description
    context['ip_search_form'] = ip_search_form
    return render(request, 'iprecord.html', context)

def export_ip(request):
    ip_address = request.GET.get('ip_address', '')
    device_name = request.GET.get('device_name', '')
    ip_description = request.GET.get('ip_description', '')
    if ip_address == device_name == ip_description == '':
        ip_all_list = IpRecord.objects.all()
    else:
        if ip_address != '':
            ip_all_list = IpRecord.objects.filter(device_ip=ip_address)
        elif device_name != '':
            ip_all_list = IpRecord.objects.filter(device_name=device_name, ip_description__icontains=ip_description)
        else:
            ip_all_list = IpRecord.objects.filter(ip_description__icontains=ip_description)
    
    output = exportXls(IpRecord._meta.fields, ip_all_list)

    # response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment; filename="iprecord_result.xls"'
    response = FileResponse(output, as_attachment=True, filename="iprecord_result.xls") # 使用Fileresponse替代以上两行
    return response

def allocate_ip(request):
    context = {}
    if request.method == 'GET':
        context['ip_allocate_form'] = IpAllocateForm()
        return render(request, 'ipallocation.html', context)
    elif request.method == 'POST':
        ip_allocate_form = IpAllocateForm(request.POST)
        if ip_allocate_form.is_valid():
            public_ip_allocation = PublicIpAllocation()
            public_ip_allocation.ies = ip_allocate_form.cleaned_data['ies']
            public_ip_allocation.order_num = ip_allocate_form.cleaned_data['order_num']    
            public_ip_allocation.client_num = ip_allocate_form.cleaned_data['client_num']    
            public_ip_allocation.product_num = ip_allocate_form.cleaned_data['product_num']
            public_ip_allocation.ip = ip_allocate_form.cleaned_data['ip']
            public_ip_allocation.mask = ip_allocate_form.cleaned_data['mask']
            public_ip_allocation.gateway = ip_allocate_form.cleaned_data['gateway']
            public_ip_allocation.link_tag = ip_allocate_form.cleaned_data['link_tag']
            public_ip_allocation.device_name = ip_allocate_form.cleaned_data['device_name']
            public_ip_allocation.logic_port = ip_allocate_form.cleaned_data['logic_port']
            public_ip_allocation.svlan = ip_allocate_form.cleaned_data['svlan']
            public_ip_allocation.cvlan = ip_allocate_form.cleaned_data['cvlan']
            public_ip_allocation.access_type = ip_allocate_form.cleaned_data['access_type']
            public_ip_allocation.olt_name = ip_allocate_form.cleaned_data['olt_name']
            public_ip_allocation.client_name = ip_allocate_form.cleaned_data['client_name']
            public_ip_allocation.ip_description = ip_allocate_form.cleaned_data['ip_description']
            public_ip_allocation.up_brandwidth = ip_allocate_form.cleaned_data['up_brandwidth']
            public_ip_allocation.down_brandwidth = ip_allocate_form.cleaned_data['down_brandwidth']
            public_ip_allocation.alc_user = request.user    # 直接通过request获取当前操作用户
            public_ip_allocation.save()
            context['status'] = 1   # 操作状态
        else:
            context['status'] = -1

        context['ip_allocate_form'] = ip_allocate_form
        return render(request, 'ipallocation.html', context)