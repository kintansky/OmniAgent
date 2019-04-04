from django.shortcuts import render, get_object_or_404, redirect
from .models import IpmanResource, IpRecord, PublicIpAllocation, PrivateIpAllocation, PublicIpModRecord, PrivateIpModRecord
from .forms import IPsearchForm, PortSearchForm, IpAllocateForm, IpPrivateAllocateForm, IpModForm, IPAllocateSearchForm
from funcpack.funcs import pages, exportXls
from django.http import FileResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import datetime
import re

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


'''
device iprecord log
'''
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
    response = FileResponse(open(output, 'rb'), as_attachment=True, filename="iprecord_result.xls") # 使用Fileresponse替代以上两行
    return response

'''
 IP分配记录
'''
def allocate_ip_list(request, ip_type):
    context = {}
    if ip_type == 'public':
        ip_all_list = PublicIpAllocation.objects.all()
        page_of_objects, page_range = pages(request, ip_all_list)
        context['public_ip'] = 1
        context['count'] = PublicIpAllocation.objects.all().count()
    elif ip_type == 'private':
        ip_all_list = PrivateIpAllocation.objects.all()
        page_of_objects, page_range = pages(request, ip_all_list)
        context['public_ip'] = 0
        context['count'] = PrivateIpAllocation.objects.all().count()

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['ip_search_form'] = IPAllocateSearchForm()
    return render(request, 'iprecord_allocated.html', context)

def search_allocated_ip(request, ip_type):
    context = {}
    ip_search_form = IPAllocateSearchForm(request.GET)
    if ip_search_form.is_valid():
        ip_address = ip_search_form.cleaned_data['ip_address']
        client_name = ip_search_form.cleaned_data['client_name']
        if ip_type == 'public': # 公网地址
            context['public_ip'] = 1
            if ip_address != '':
                ip_all_list =  PublicIpAllocation.objects.filter(ip=ip_address, client_name__icontains=client_name)
            elif client_name != '':
                ip_all_list =  PublicIpAllocation.objects.filter(client_name__icontains=client_name)
            else:
                ip_all_list =  PublicIpAllocation.objects.all()
        elif ip_type == 'private':  # 私网地址
            context['public_ip'] = 0
            if ip_address != '':
                ip_all_list = PrivateIpAllocation.objects.filter(ip=ip_address, client_name__icontains=client_name)
            elif client_name != '':
                ip_all_list = PrivateIpAllocation.objects.filter(client_name__icontains=client_name)
            else:
                ip_all_list = PrivateIpAllocation.objects.all()
    else:
        if ip_type == 'public':
            context['public_ip'] = 1
        elif ip_type == 'private':
            context['public_ip'] = 0
        context['ip_search_form'] = ip_search_form
        return render(request, 'iprecord_allocated.html', context)
        
    page_of_objects, page_range = pages(request, ip_all_list)

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['search_ip_address'] = ip_address
    context['search_client_name'] = client_name
    context['ip_search_form'] = ip_search_form
    return render(request, 'iprecord_allocated.html', context)

def allocate_ip(request, ip_type):
    context = {}
    if ip_type == 'public': # 公网地址分配
        context['public_ip'] = 1
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
                public_ip_allocation.state = 'InUse'
                public_ip_allocation.save()
                context['status'] = 1   # 操作状态
            else:
                context['status'] = -1

            context['ip_allocate_form'] = ip_allocate_form
            return render(request, 'ipallocation.html', context)

    elif ip_type == 'private':  # 私网地址分配
        context['public_ip'] = 0
        if request.method == 'GET':
            context['ip_allocate_form'] = IpPrivateAllocateForm()
            return render(request, 'ipallocation.html', context)
        elif request.method == 'POST':
            ip_allocate_form = IpPrivateAllocateForm(request.POST)
            if ip_allocate_form.is_valid():
                private_ip_allocation = PrivateIpAllocation()
                private_ip_allocation.service = ip_allocate_form.cleaned_data['service']
                private_ip_allocation.community = ip_allocate_form.cleaned_data['community']    
                private_ip_allocation.service_id = ip_allocate_form.cleaned_data['service_id']    
                private_ip_allocation.rd = ip_allocate_form.cleaned_data['rd']
                private_ip_allocation.rt = ip_allocate_form.cleaned_data['rt']
                private_ip_allocation.order_num = ip_allocate_form.cleaned_data['order_num']
                private_ip_allocation.client_name = ip_allocate_form.cleaned_data['client_name']
                private_ip_allocation.client_num = ip_allocate_form.cleaned_data['client_num']
                private_ip_allocation.product_num = ip_allocate_form.cleaned_data['product_num']
                private_ip_allocation.device_name = ip_allocate_form.cleaned_data['device_name']
                private_ip_allocation.logic_port = ip_allocate_form.cleaned_data['logic_port']
                private_ip_allocation.svlan = ip_allocate_form.cleaned_data['svlan']
                private_ip_allocation.cvlan = ip_allocate_form.cleaned_data['cvlan']
                private_ip_allocation.olt_name = ip_allocate_form.cleaned_data['olt_name']
                private_ip_allocation.access_type = ip_allocate_form.cleaned_data['access_type']
                private_ip_allocation.ip = ip_allocate_form.cleaned_data['ip']
                private_ip_allocation.gateway = ip_allocate_form.cleaned_data['gateway']
                private_ip_allocation.ipsegment = ip_allocate_form.cleaned_data['ipsegment']
                private_ip_allocation.ip_description = ip_allocate_form.cleaned_data['ip_description']
                private_ip_allocation.alc_user = request.user    # 直接通过request获取当前操作用户
                private_ip_allocation.state = 'InUse'
                private_ip_allocation.save()
                context['status'] = 1   # 操作状态
            else:
                context['status'] = -1

            context['ip_allocate_form'] = ip_allocate_form
            return render(request, 'ipallocation.html', context)

def ajax_locate_ip(request, ip_type):
    data = {}
    rid = request.GET.get('rid')
    if ip_type == 'public':
        try:
            record = PublicIpAllocation.objects.get(id=rid)
            data = objectDataSerializer(record, data)   # 序列化单个模型的字段，输出json
            if data['access_type'] == 'PTN':
                pass
            elif data['access_type'] == 'GPON':
                m1 = re.match(r'lag-\d+:(\d*)\.(\d*)', data['logic_port'])
                if m1:
                    pass
                else:
                    m2 = re.match(r'Eth-Trunk\d*\.(\d*)', data['logic_port'])
                    if m2:
                        data['logic_port'] = data['logic_port']+'.'+str(data['cvlan'])
                    else:
                        m3 = re.match(r'((\d{1,2}/){1,}\d{1,2})', data['logic_port'])
                        if m3:
                            data['logic_port'] = data['logic_port']+':'+str(data['svlan'])+'.'+str(data['cvlan'])
            allocation_form = IpAllocateForm(data)
            data = formHtmlCallBack(allocation_form, data, ip_type) # 用于ajax回调函数填充网页
        except ObjectDoesNotExist as err:
            data['status'] = 'error'
            data['error_info'] = str(err)
    elif ip_type == 'private':
        try:
            record = PrivateIpAllocation.objects.get(id=rid)
            data = objectDataSerializer(record, data)   # 序列化单个模型的字段，输出json
            allocation_form = IpPrivateAllocateForm(data)
            data = formHtmlCallBack(allocation_form, data, ip_type) # 用于ajax回调函数填充网页
        except ObjectDoesNotExist as err:
            data['status'] = 'error'
            data['error_info'] = str(err)
    return JsonResponse(data)

def objectDataSerializer(obj, data):    # 序列化单个模型的字段，输出json
    for f in obj._meta.fields:
        key = f.attname
        val = obj.serializable_value(key)
        data[key] = val
    return data

def formHtmlCallBack(allocation_form, data, ip_type):   # 用于ajax回调函数填充网页
    h = '<div class="row"><form class="modal_form" action="" method="POST" rid="{}" ip_type="{}">'.format(data['id'], ip_type)
    for f in allocation_form:
        h += '<div class="form-group"><label for="{}" class="col-sm-2 control-label">{}</label><div class="col-sm-4">{}</div></div>'.format(f.id_for_label, f.label, f)
    h += '</form></div><hr>'
    h += '<div class="row"><form class="modal_form" action="" method="POST" rid="{}" ip_type="{}">'.format(data['id'], ip_type)
    ip_mod_form = IpModForm()
    for f in ip_mod_form:
        h += '<div class="form-group"><label for="{}" class="col-sm-2 control-label">{}</label><div class="col-sm-4">{}</div></div>'.format(f.id_for_label, f.label, f)
    h += '</form></div>'
    data['status'] = 'success'
    data['allocation_form'] = h
    return data

def ip_allocation_mod(request, ip_type):
    if request.method == 'POST':
        data = {}
        # print(request.POST)
        rid = request.POST.get('rid')
        if ip_type == 'public':
            target_record = PublicIpAllocation.objects.get(id=rid)

            ip_mod_form = IpModForm(request.POST)
            ip_allocate_form = IpAllocateForm(request.POST)
            if ip_allocate_form.is_valid() and ip_mod_form.is_valid():
                # 备份旧数据
                mod_record = PublicIpModRecord()
                mod_record.ever_ies = target_record.ies
                mod_record.ever_client_num = target_record.client_num
                mod_record.ever_product_num = target_record.product_num
                mod_record.ever_ip = target_record.ip
                mod_record.ever_mask = target_record.mask
                mod_record.ever_gateway = target_record.gateway
                mod_record.ever_link_tag = target_record.link_tag
                mod_record.ever_device_name = target_record.device_name
                mod_record.ever_logic_port = target_record.logic_port
                mod_record.ever_svlan = target_record.svlan
                mod_record.ever_cvlan = target_record.cvlan
                mod_record.ever_access_type = target_record.access_type
                mod_record.ever_olt_name = target_record.olt_name
                mod_record.ever_client_name = target_record.client_name
                mod_record.ever_ip_description = target_record.ip_description
                mod_record.ever_up_brandwidth = target_record.up_brandwidth
                mod_record.ever_down_brandwidth = target_record.down_brandwidth
                mod_record.ever_state = target_record.state
                # 调整单号
                mod_record.mod_target = target_record
                mod_record.mod_order = ip_mod_form.cleaned_data['mod_order']
                mod_record.mod_msg = ip_mod_form.cleaned_data['mod_msg']
                mod_record.mod_user = request.user
                mod_record.save()
                # 新数据
                target_record.ies = ip_allocate_form.cleaned_data['ies']
                target_record.order_num = ip_allocate_form.cleaned_data['order_num']    
                target_record.client_num = ip_allocate_form.cleaned_data['client_num']    
                target_record.product_num = ip_allocate_form.cleaned_data['product_num']
                target_record.ip = ip_allocate_form.cleaned_data['ip']
                target_record.mask = ip_allocate_form.cleaned_data['mask']
                target_record.gateway = ip_allocate_form.cleaned_data['gateway']
                target_record.link_tag = ip_allocate_form.cleaned_data['link_tag']
                target_record.device_name = ip_allocate_form.cleaned_data['device_name']
                target_record.logic_port = ip_allocate_form.cleaned_data['logic_port']
                target_record.svlan = ip_allocate_form.cleaned_data['svlan']
                target_record.cvlan = ip_allocate_form.cleaned_data['cvlan']
                target_record.access_type = ip_allocate_form.cleaned_data['access_type']
                target_record.olt_name = ip_allocate_form.cleaned_data['olt_name']
                target_record.client_name = ip_allocate_form.cleaned_data['client_name']
                target_record.ip_description = ip_allocate_form.cleaned_data['ip_description']
                target_record.up_brandwidth = ip_allocate_form.cleaned_data['up_brandwidth']
                target_record.down_brandwidth = ip_allocate_form.cleaned_data['down_brandwidth']
                target_record.state = ip_allocate_form.cleaned_data['state']
                target_record.save()

                data['status'] = 'success'   # 操作状态
            else:
                data['status'] = 'error'
                # 返回给js回调函数的错误信息
                error_info = ''
                error1Dict = ip_allocate_form.errors.as_data()  # dict
                for f in error1Dict:
                    error_info += '填写错误字段{}: {}'.format(f, error1Dict[f])
                error2Dict = ip_mod_form.errors.as_data()
                for f in error2Dict:
                    error_info += '填写错误字段{}: {}'.format(f, error2Dict[f])
                data['error_info'] = error_info
        
        elif ip_type == 'private':
            target_record = PrivateIpAllocation.objects.get(id=rid)
            
            ip_mod_form = IpModForm(request.POST)
            ip_allocate_form = IpPrivateAllocateForm(request.POST)
            if ip_allocate_form.is_valid() and ip_mod_form.is_valid():
                mod_record = PrivateIpModRecord()
                # 备份数据
                mod_record.ever_service = target_record.service
                mod_record.ever_community = target_record.community
                mod_record.ever_service_id = target_record.service_id
                mod_record.ever_rd = target_record.rd
                mod_record.ever_rt = target_record.rt
                mod_record.ever_client_name = target_record.client_name
                mod_record.ever_client_num = target_record.client_num
                mod_record.ever_product_num = target_record.product_num
                mod_record.ever_device_name = target_record.device_name
                mod_record.ever_logic_port = target_record.logic_port
                mod_record.ever_svlan = target_record.svlan
                mod_record.ever_cvlan = target_record.cvlan
                mod_record.ever_olt_name = target_record.olt_name
                mod_record.ever_access_type = target_record.access_type
                mod_record.ever_ip = target_record.ip
                mod_record.ever_gateway = target_record.gateway
                mod_record.ever_ipsegment = target_record.ipsegment
                mod_record.ever_ip_description = target_record.ip_description
                mod_record.ever_state = target_record.state
                # 修改信息
                mod_record.mod_target = target_record
                mod_record.mod_order = ip_mod_form.cleaned_data['mod_order']
                mod_record.mod_msg = ip_mod_form.cleaned_data['mod_msg']
                mod_record.mod_user = request.user
                mod_record.save()
                # 新信息
                target_record.service = ip_allocate_form.cleaned_data['service']
                target_record.community = ip_allocate_form.cleaned_data['community']    
                target_record.service_id = ip_allocate_form.cleaned_data['service_id']    
                target_record.rd = ip_allocate_form.cleaned_data['rd']
                target_record.rt = ip_allocate_form.cleaned_data['rt']
                target_record.order_num = ip_allocate_form.cleaned_data['order_num']
                target_record.client_name = ip_allocate_form.cleaned_data['client_name']
                target_record.client_num = ip_allocate_form.cleaned_data['client_num']
                target_record.product_num = ip_allocate_form.cleaned_data['product_num']
                target_record.device_name = ip_allocate_form.cleaned_data['device_name']
                target_record.logic_port = ip_allocate_form.cleaned_data['logic_port']
                target_record.svlan = ip_allocate_form.cleaned_data['svlan']
                target_record.cvlan = ip_allocate_form.cleaned_data['cvlan']
                target_record.olt_name = ip_allocate_form.cleaned_data['olt_name']
                target_record.access_type = ip_allocate_form.cleaned_data['access_type']
                target_record.ip = ip_allocate_form.cleaned_data['ip']
                target_record.gateway = ip_allocate_form.cleaned_data['gateway']
                target_record.ipsegment = ip_allocate_form.cleaned_data['ipsegment']
                target_record.ip_description = ip_allocate_form.cleaned_data['ip_description']
                target_record.state = ip_allocate_form.cleaned_data['state']
                target_record.save()

                data['status'] = 'success'   # 操作状态
            else:
                data['status'] = 'error'
                error_info = ''
                error1Dict = ip_allocate_form.errors.as_data()
                for f in error1Dict:
                    error_info += '填写错误字段{}: {}'.format(f, error1Dict[f])
                error2Dict = ip_mod_form.errors.as_data()
                for f in error2Dict:
                    error_info += '填写错误字段{}: {}'.format(f, error2Dict[f])
                data['error_info'] = error_info
        return JsonResponse(data)