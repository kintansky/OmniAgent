from django.shortcuts import render, get_object_or_404
from .models import IpmanResource
from .models import IpRecord
from .forms import IPsearchForm, PortSearchForm
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
        else:
            ip_all_list = IpRecord.objects.filter(ip_description__icontains=ip_description)
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