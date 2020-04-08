from django.shortcuts import render, get_object_or_404, redirect
from .models import IpmanResource, IpRecord, IPAllocation, IPMod, GroupClientIPSegment, GroupClientIpReserve, PublicIpSegment, PublicIPSegmentSchema, ICP
from .forms import IPsearchForm, IPAllocateSearchForm, IPTargetForm, NewIPAllocationForm, ClientSearchForm, DeviceIpSegmentForm, NewIpSegmentForm, WorkLoadSearchForm, NewSchemaSegmentForm, ICPInfoForm
from funcpack.funcs import pages, exportXls, objectDataSerializer, objectDataSerializerRaw, dict2SearchParas, getDateRange, rawQueryExportXls, exportClassifiedXls
from django.http import FileResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import re
from omni.settings.base import BASE_DIR
import os
from django.utils import timezone
from IPy import IP
import json
from django.db.models import Q, Count, Sum
import base64
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

def ajax_search_slot_ports(request):
    data = {}
    device_name = request.GET.get('device_name')
    slot = int(request.GET.get('slot').replace('collapse', ''))
    target_ports = IpmanResource.objects.filter(
        device_name=device_name, slot=slot)
    rawQueryCmd = '''SELECT ni.id, ni.port, ni.brand_width, ni.port_status, 
                ni.port_phy_status, ni.logic_port, ni.port_description, np.stateCRC 
                FROM omni_agent.MR_REC_ipman_resource AS ni LEFT JOIN omni_agent.OM_REP_port_error_diff as np 
                ON np.device_name = ni.device_name AND np.port = ni.port AND np.record_time BETWEEN %s and %s 
                WHERE ni.device_name = %s AND ni.slot = %s
    '''
    today_time = timezone.datetime.now()
    time_end = timezone.datetime(year=today_time.year, month=today_time.month,
                                 day=today_time.day, hour=23, minute=59, second=59)
    time_begin = time_end + timezone.timedelta(days=-2)
    rawQueryData = (time_begin, time_end, device_name, slot)
    target_ports = IpmanResource.objects.raw(rawQueryCmd, rawQueryData)
    data = formHtmlCallBack_slot(target_ports, data)
    return JsonResponse(data)


def formHtmlCallBack_slot(target_ports, data):
    # 生成表给内容填充回去前端
    h = ''
    td = '<td>{}</td>'
    for tp in target_ports:
        port = td.format(tp.port)
        bw = td.format(tp.brand_width)
        ps = td.format(tp.port_status)
        phs = td.format(tp.port_phy_status)
        lp = td.format(tp.logic_port)
        p_des = td.format(tp.port_description)
        if tp.stateCRC == 0 or tp.stateCRC is None:
            crc = td.format(tp.stateCRC)
        else:
            crc = '<td class="danger">{}</td>'.format(tp.stateCRC)
        h += '<tr>{}{}{}{}{}{}{}</tr>'.format(port,
                                              bw, ps, phs, lp, p_des, crc)
    data['ports_table'] = h
    data['status'] = 'success'
    return data


#
# @permission_required('networkresource.view_iprecord', login_url='/login/')
@staff_member_required(redirect_field_name='from', login_url='login')
def ip_list(request):
    ip_all_list = IpRecord.objects.all()
    page_of_objects, page_range = pages(request, ip_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['ip_search_form'] = IPsearchForm()
    return render(request, 'iprecord.html', context)


def search_ip(request):
    ip_search_form = IPsearchForm(request.GET)
    if ip_search_form.is_valid():
        ip_address = ip_search_form.cleaned_data['ip_address']
        device_name = ip_search_form.cleaned_data['device_name']
        ip_description = ip_search_form.cleaned_data['description']
        ip_type = ip_search_form.cleaned_data['ip_type']
        if ip_address != '':
            ip_all_list = IpRecord.objects.filter(device_ip=ip_address)
        elif ip_type == 'all':
            if device_name != '':
                ip_all_list = IpRecord.objects.filter(
                    device_name__icontains=device_name, ip_description__icontains=ip_description)
            elif ip_description != '':
                ip_all_list = IpRecord.objects.filter(
                    ip_description__icontains=ip_description)
            else:
                ip_all_list = IpRecord.objects.all()
        else:
            if device_name != '':
                ip_all_list = IpRecord.objects.filter(
                    device_name__icontains=device_name, ip_type=ip_type, ip_description__icontains=ip_description)
            elif ip_description != '':
                ip_all_list = IpRecord.objects.filter(
                    ip_type=ip_type, ip_description__icontains=ip_description)
            else:
                ip_all_list = IpRecord.objects.filter(ip_type=ip_type)
    else:
        context = {}
        context['ip_search_form'] = ip_search_form
        return render(request, 'iprecord.html', context)

    page_of_objects, page_range = pages(request, ip_all_list)

    context = {}
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['search_ip_address'] = ip_address
    context['search_device_name'] = device_name
    context['search_description'] = ip_description
    context['search_ip_type'] = ip_type
    context['ip_search_form'] = ip_search_form
    return render(request, 'iprecord.html', context)


def export_ip(request):
    ip_address = request.GET.get('ip_address', '')
    device_name = request.GET.get('device_name', '')
    ip_description = request.GET.get('ip_description', '')
    ip_type = request.GET.get('ip_type', '')
    # print(ip_address, device_name, ip_description, ip_type)
    if ip_address == device_name == ip_description == '':
        file = os.path.join(
            BASE_DIR, 'collected_static/downloads/files/iprecord_all.xls')
        cmd = '''
        select * from MR_REC_ip_record order by id
        '''
        ip_all_list = IpRecord.objects.raw(cmd)
        output = exportClassifiedXls(ip_all_list.columns, ip_all_list, ('record_time',), 'ip_type',)
        response = FileResponse(
            open(output, 'rb'), as_attachment=True, filename="iprecord_all.xls")
        return response
    elif ip_type == 'all':
        if ip_address != '':
            ip_all_list = IpRecord.objects.filter(device_ip=ip_address)
        elif device_name != '':
            ip_all_list = IpRecord.objects.filter(
                device_name=device_name, ip_description__icontains=ip_description)
        elif ip_description != '':
            ip_all_list = IpRecord.objects.filter(
                ip_description__icontains=ip_description)

    else:
        if ip_address != '':
            ip_all_list = IpRecord.objects.filter(device_ip=ip_address)
        elif device_name != '':
            ip_all_list = IpRecord.objects.filter(
                device_name=device_name, ip_type=ip_type, ip_description__icontains=ip_description)

    output = exportXls(IpRecord._meta.fields, ip_all_list, ('record_time',))
    response = FileResponse(open(output, 'rb'), as_attachment=True,
                            filename="iprecord__search_result.xls")  # 使用Fileresponse替代以上两行
    return response


# IP分配
def new_allocate_ip(request):
    context = {}
    if request.method == 'GET':
        ip_target_form = IPTargetForm()
        new_ip_allocation_form = NewIPAllocationForm()
        new_icp_info_form = ICPInfoForm()
        context['new_icp_info_form'] = new_icp_info_form
        context['ip_target_form'] = ip_target_form
        context['new_ip_allocation_form'] = new_ip_allocation_form
    return render(request, 'ipallocate.html', context)


GET_OLT_CAN_ALLOCATED_IP = '''
    SELECT seg.id, seg.ip, seg.subnet_gateway, seg.subnet_mask FROM MR_REC_group_client_ip_segment AS seg
    inner JOIN (
    SELECT gateway, ip_mask AS mask, olt FROM MR_STS_ip_olt_detail 
    WHERE olt = %s
    AND gateway NOT IN (
    SELECT gateway FROM (
    SELECT gateway, ip_mask, COUNT(DISTINCT olt) AS cnt 
    FROM MR_STS_ip_olt_detail 
    WHERE ip_mask != 32 
    GROUP BY gateway 
    HAVING cnt > 1) AS a) 
    GROUP BY gateway, ip_mask, olt) AS target_gw
    ON seg.subnet_gateway = target_gw.gateway AND target_gw.mask = seg.subnet_mask 
    AND seg.segment_state = TRUE AND seg.ip_state = 0 
'''

def ajax_get_olt_can_allocated_ip(request):
    data = {}
    olt = request.GET.get('olt', '').strip()
    ips = GroupClientIPSegment.objects.raw(GET_OLT_CAN_ALLOCATED_IP, (olt,))
    ip_list = ['{}/{} 网关{}'.format(d.ip, d.subnet_mask, d.subnet_gateway) for d in ips]
    data['ip_list'] = ','.join(ip_list)
    data['status'] = 'success'
    return JsonResponse(data)


def ajax_generate_ip_list2(request):
    data = {}
    ip_target_form = IPTargetForm(request.POST)
    include_private_ip = 'n'
    if ip_target_form.is_valid():
        ip_func = ip_target_form.cleaned_data['ip_func']
        first_ip = ip_target_form.cleaned_data['first_ip']
        ip_num = ip_target_form.cleaned_data['ip_num']
        ip_segment = ip_target_form.cleaned_data['ip_segment']
        state = ip_target_form.cleaned_data['state']
        gateway = ip_target_form.cleaned_data['gateway']
        if ip_num < 0:
            subnet = IP.make_net(*first_ip.split('/'))
            first_ip = subnet[0].strNormal()
            last_ip = subnet[-1].strNormal()
            data['target'] = subnet.strNormal()
        else:
            temp_ip, mask = first_ip.split('/')
            ip_sep = temp_ip.split('.')
            last_num = int(ip_sep[3]) + ip_num
            if last_num > 255:
                last_ip = '.'.join(ip_sep[0:2]+[str(int(ip_sep[2])+1), str(last_num-255-1)])
            else:
                last_ip = '.'.join(ip_sep[0:3]+[str(last_num),])
            data['target'] = first_ip + 'p' + str(ip_num)
        if ip_func == '私网':
            include_private_ip = 'y'
        data['include_private_ip'] = include_private_ip
        data['ip_func'] = ip_func
        data['first_ip'] = first_ip
        data['last_ip'] = last_ip
        data['gw'] = gateway
        data['state'] = state
        data['status'] = 'success'
    else:
        data['status'] = 'error'
        error_info = ''
        errorDict = ip_target_form.errors.get_json_data()
        for f in errorDict:
            error_info += '填写错误字段{}: {}'.format(f, errorDict[f][0]['message'])
        data['error_info'] = error_info
    return JsonResponse(data)

def confirm_ready_ip(request):
    data = {}
    target_list = request.POST.get('target-list', '{}')
    include_private_ip = 'n'
    if target_list == '':
        target_list = '{}'
    target_dict = json.loads(target_list)
    target_list_append = request.POST.get('target_list_append', '{}')
    target_dict_append = json.loads(target_list_append)

    for appendKey in target_dict_append:
        targetKey = [k for k in target_dict]
        targetIP = [t.split('p')[0] for t in targetKey]
        if 'p' in appendKey:
            searchKey = appendKey.split('p')
            if searchKey[0] in targetIP:
                i = targetIP.index(searchKey[0])
                if int(searchKey[1]) >= int(targetKey[i].split('p')[1]):
                    target_dict.pop(targetKey[i])
                    target_dict[appendKey] = target_dict_append[appendKey]
            else:
                target_dict[appendKey] = target_dict_append[appendKey]
        else:
            if appendKey not in targetKey:
                target_dict[appendKey] = target_dict_append[appendKey]
    table_data = {}
    for t in target_dict:
        if 'p' in t:
            ip, ip_num = t.split('p')
            temp_ip, mask = ip.split('/')
            ip_sep = temp_ip.split('.')
            last_num = int(ip_sep[3]) + int(ip_num)
            last_ip = ''
            if last_num > 255:
                last_ip = '.'.join(ip_sep[0:2]+[str(int(ip_sep[2])+1), str(last_num-255-1)])
            else:
                last_ip = '.'.join(ip_sep[0:3]+[str(last_num),])
            table_data[t] = [target_dict[t][0], ip, last_ip, target_dict[t][2], target_dict[t][1]]
        else:
            subnet = IP.make_net(*t.split('/'))
            first_ip = subnet[0].strNormal()
            last_ip = subnet[-1].strNormal()
            table_data[t] = [target_dict[t][0], first_ip, last_ip,  target_dict[t][2], target_dict[t][1]]
    for t in target_dict:
        if '私网' in target_dict[t]:
            include_private_ip = 'y'
            break

    data['status'] = 'success'
    data['target_list'] = json.dumps(target_dict)
    data['table_data'] = json.dumps(table_data)
    data['include_private_ip'] = include_private_ip
    
    return JsonResponse(data)

def remove_conf_ip(request):
    data = {}
    include_private_ip = 'n'
    target_dict = json.loads(request.POST.get('target-list', '{}'))
    remove_target = request.POST.get('remove-target', '').replace(' ', 'p')
    for t in target_dict:
        if t == remove_target:
            target_dict.pop(t)
            break
    for t in target_dict:
        if '私网' in target_dict[t]:
            include_private_ip = 'y'
            break
    data['include_private_ip'] = include_private_ip
    data['target_list'] = json.dumps(target_dict)
    data['status'] = 'success'
    return JsonResponse(data)


def ajax_get_olt_bng(request, device_type):
    data = {}
    if device_type == 'olt':
        olt = request.GET.get('olt', '').strip()
        if 'PTN' in olt.upper():
            data['olt_list'] = '无候选结果'
            data['access_type'] = 'PTN'
            data['status'] = 'success'
            return JsonResponse(data)
        elif re.match(r'.*?(-BNG\d+)|(-BRAS\d+).*?', olt.upper()):
            data['olt_list'] = '无候选结果'
            data['access_type'] = 'DIRECT'
            data['status'] = 'success'
            return JsonResponse(data)
        rawQueryCmd = 'select id, olt from omni_agent.MR_REP_olt_bng_references where olt LIKE "%%{}%%" GROUP BY olt'.format(olt)
        olts = IpmanResource.objects.raw(rawQueryCmd)
        olt_list = [d.olt for d in olts]
        if len(olt_list) > 10:
            data['olt_list'] = '候选结果过多，请使用关键字'
            data['status'] = 'error'
        elif len(olt_list) == 0:
            data['olt_list'] = '无候选结果'
            data['status'] = 'error'
            data['olt_count'] = 0
        else:
            data['olt_list'] = ','.join(olt_list)
            data['access_type'] = 'GPON'
            data['status'] = 'success'
        return JsonResponse(data)
    elif device_type == 'bng':
        olt = request.GET.get('olt', '').strip()
        rawQueryCmd = 'select id, bng from omni_agent.MR_REP_olt_bng_references where olt = %s GROUP BY bng'
        bngs = IpmanResource.objects.raw(rawQueryCmd, (olt,))
        bng_list = '/'.join([b.bng for b in bngs])
        data['bng_list'] = bng_list
        data['status'] = 'success'
        # TODO: 应该在这里选择PTN还是OLT接入

    return JsonResponse(data)


def searchICPInfo(rePattern, text, groupNum):
    m = re.search(rePattern, text)
    if m:
        return m.group(groupNum)
    else:
        return None

def parse_icp(request):
    data = {}
    icp_text = request.GET.get('icp_text', '')
    # 字段对应的正则表达式，因为提供的字符串可能格式不稳定，尽量不要多字段匹配
    icp_research_pattern = {
        'id_identify_id': [r'单位证件号码\s+(\S+)', 1],
        'id_guard_level': [r'保障等级\s+(\S+)', 1],
        'id_city': [r'受理地市\s+(\S+)', 1],
        'id_district': [r'受理区域\s+(\S+)', 1],
        'id_distributor': [r'派单人\s+(\S+)', 1],
        'id_distributor_contact': [r'派单人\s+\S+\s+?联系方式\s*?(\d+)', 1],
        'id_demand': [r'需求描述\s+([\s\S]*?)客户信息', 1],
        'id_bandwidth_up': [r'上行带宽\s+(\d+)', 1],
        'id_bandwidth_dwn': [r'上行带宽\s+\d+\s+下行带宽\s+(\d+)', 1],
        'id_client_tech': [r'客户配合联系人\s+(\S+)', 1],
        'id_client_tech_contact': [r'客户配合联系人\s+\S+\s+客户配合联系方式\s+(\d+)', 1],
        'id_demand_ipv4_amount': [r'IPV4地址数量\(个\)\D*(\d+)\s*IPV6地址数量', 1],  # 确认数据位置
        'id_demand_ipv6_amount': [r'IPV6地址数量\(个\)\D*(\d+)\s*IP接入能力', 1],  # 确认数据位置
        'id_client_address': [r'单位详细地址\s+(\S+)', 1],
        'id_businessman': [r'联系人姓名\(客户侧\)\s+(\S+)', 1],
        'id_businessman_contact': [r'联系人姓名\(客户侧\)\s+\S+\s+联系人电话\(客户侧\)\s+(\d+)', 1],
    }
    # 解析icp_text成一个字典，字典都以id_字段名为key
    icp_result = dict()
    for key in icp_research_pattern:
        s = searchICPInfo(icp_research_pattern[key][0], icp_text, icp_research_pattern[key][1])
        if s is not None:
            icp_result[key] = s
            continue
    data['parsed_icp_result'] = json.dumps(icp_result)
    return JsonResponse(data)

def confirm_icp(request):
    data = {}
    # print(request.POST)
    new_icp_info_form = ICPInfoForm(request.POST)
    if new_icp_info_form.is_valid():
        # 新增前确认是否存在一摸一样的数据
        try:
            already_has_icp = ICP.objects.get(**new_icp_info_form.cleaned_data)
            # data['choose_icp_id'] = already_has_icp.pk
            objectDataSerializer(already_has_icp, data)
        except ObjectDoesNotExist:  # 如果不存在则创建
            new_icp = ICP(**new_icp_info_form.cleaned_data)
            new_icp.save()
            already_has_icp = ICP.objects.get(**new_icp_info_form.cleaned_data)
            # data['choose_icp_id'] = already_has_icp.pk
            objectDataSerializer(already_has_icp, data)
        data['status'] = 'success'
    else:
        data['status'] = 'error'
        errorDict = new_icp_info_form.errors.get_json_data()
        data['error_info'] = json.dumps(errorDict)
    return JsonResponse(data)


def ajax_confirm_allocate(request):
    data = {}
    new_ip_allocation_form = NewIPAllocationForm(request.POST)
    target_list = request.POST.get('target-list', '{}')
    if target_list != '' and target_list != '{}':
        target_dict = json.loads(target_list)
        # print(target_dict)
        if new_ip_allocation_form.is_valid():
            # print(new_ip_allocation_form.cleaned_data)
            bngs = new_ip_allocation_form.cleaned_data['bng'].split('/')    # 单台BNG不受影响，分裂的时候如果单台，另一台是空
            for target in target_dict:
                ipData = target_dict[target]    # target_dict[data['target']] = [ip_func, state, gateway]
                if 'p' in target:
                    first_ip, ip_num = target.split('p')
                    first_ip, mask = first_ip.split('/')
                    ip_sep = first_ip.split('.')
                    ready_to_allocate_ips = ['.'.join(ip_sep[0:3]+[str(int(ip_sep[3])+i),]) for i in range(int(ip_num)+1)]
                else:
                    first_ip, mask = target.split('/')
                    subnet = IP.make_net(first_ip, mask)
                    ready_to_allocate_ips = [ip.strNormal() for ip in subnet]
                for targetIp in ready_to_allocate_ips:
                    for bng in bngs:
                        ip_allocation = IPAllocation()
                        ip_allocation.ip = targetIp
                        ip_allocation.ip_mask = int(mask)
                        ip_allocation.ip_func = ipData[0]
                        if ipData[0] == '私网':
                            ip_allocation.community = new_ip_allocation_form.cleaned_data['community']
                            ip_allocation.rt = new_ip_allocation_form.cleaned_data['rt']
                            ip_allocation.rd = new_ip_allocation_form.cleaned_data['rd']
                        else:
                            ip_allocation.community = ""
                            ip_allocation.rt = ""
                            ip_allocation.rd = ""
                        ip_allocation.state = ipData[1]
                        ip_allocation.gateway = ipData[2]

                        ip_allocation.order_num = new_ip_allocation_form.cleaned_data['order_num']
                        ip_allocation.client_name = new_ip_allocation_form.cleaned_data['client_name']
                        ip_allocation.olt = new_ip_allocation_form.cleaned_data['olt']
                        ip_allocation.bng = bng
                        ip_allocation.access_type = new_ip_allocation_form.cleaned_data['access_type']
                        ip_allocation.logic_port = new_ip_allocation_form.cleaned_data['logic_port']
                        ip_allocation.svlan = new_ip_allocation_form.cleaned_data['svlan']
                        ip_allocation.cevlan = new_ip_allocation_form.cleaned_data['cevlan']
                        ip_allocation.description = new_ip_allocation_form.cleaned_data['description']
                        ip_allocation.brand_width = new_ip_allocation_form.cleaned_data['brand_width']
                        ip_allocation.service_id = new_ip_allocation_form.cleaned_data['service_id']
                        ip_allocation.group_id = new_ip_allocation_form.cleaned_data['group_id']
                        ip_allocation.product_id = new_ip_allocation_form.cleaned_data['product_id']
                        ip_allocation.network_type = new_ip_allocation_form.cleaned_data['network_type']
                        ip_allocation.comment = new_ip_allocation_form.cleaned_data['comment']
                        ip_allocation.alc_user = request.user.first_name
                        ip_allocation.alc_time = timezone.datetime.now()
                        ip_allocation.last_mod_time = ip_allocation.alc_time
                        if new_ip_allocation_form.cleaned_data['icp_id'] is not None:
                            ip_allocation.icp = get_object_or_404(ICP, pk=new_ip_allocation_form.cleaned_data['icp_id'])

                        ip_allocation.save()

            data['status'] = 'success'
        else:
            data['status'] = 'error'
            errorDict = new_ip_allocation_form.errors.get_json_data()
            data['error_info'] = json.dumps(errorDict)
    else:
        data['status'] = 'error'
        data['other_error'] = '分配失败，未提供目标IP'
    return JsonResponse(data)

# @permission_required('networkresource.view_iprecord', login_url='/login/')
@staff_member_required(redirect_field_name='from', login_url='login')
def ip_allocated_client_list(request):
    context = {}
    client_all_list = IPAllocation.objects.all().values('order_num', 'client_name', 'group_id', 'product_id').annotate(Count('id')).order_by()
    page_of_objects, page_range = pages(request, client_all_list)
    context['count'] = client_all_list.count()

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['client_search_form'] = ClientSearchForm()
    context['new_icp_info_form'] = ICPInfoForm()
    return render(request, 'ip_allocated_client_list.html', context)


def export_ip_allocation(request, amount):
    if amount == 'all':
        cmd_all = '''
        SELECT a.id, a.order_num, a.client_name, a.state, a.ip, a.ip_mask, a.gateway, 
        a.bng, a.logic_port, a.svlan, a.cevlan, a.description, a.ip_func, 
        a.olt, a.service_id, a.brand_width, a.group_id, a.product_id, a.network_type, 
        a.community, a.rt, a.rd, a.comment, a.alc_user, a.alc_time, a.access_type, a.last_mod_time,
        b.identify_id, b.guard_level, b.city, b.district, b.distributor, b.distributor_contact, 
        b.demand, b.bandwidth_up, b.bandwidth_dwn, b.client_tech, b.client_tech_contact, 
        b.demand_ipv4_amount, b.demand_ipv6_amount, b.client_address, b.businessman, b.businessman_contact 
        from MR_REC_ip_allocation as a
        left join MR_REC_icp_info as b
        on a.icp_id = b.id
        order BY a.id desc
        '''
        ip_allocation = IPAllocation.objects.raw(cmd_all)
        cmd_his = '''
        select a.id, a.mod_order_num, a.mod_user, a.mod_time, a.mod_type, a.mod_msg, a.order_num AS old_order_num, a.client_name as old_client_name, a.state as old_state, a.ip as old_ip, a.ip_mask as old_ip_mask,
        a.gateway as old_gateway, a.bng as old_bng, a.logic_port as old_logic_port, a.svlan as old_svlan, a.cevlan as old_cevlan, 
        a.description as old_description, a.ip_func as old_ip_func, a.olt as old_olt, a.access_type as old_access_type, a.service_id as old_service_id, a.brand_width as old_brand_width, 
        a.group_id as old_group_id, a.product_id as old_product_id, a.network_type as old_network_type, a.community as old_community, a.rt as old_rt, a.rd as old_rd,
        b.identify_id, b.guard_level, b.city, b.district, b.distributor, b.distributor_contact, 
        b.demand, b.bandwidth_up, b.bandwidth_dwn, b.client_tech, b.client_tech_contact, 
        b.demand_ipv4_amount, b.demand_ipv6_amount, b.client_address, b.businessman, b.businessman_contact 
        from MR_REC_ip_mod_record as a
        left join MR_REC_icp_info as b
        on a.icp_id = b.id
        order BY a.id desc
        '''
        mod_his = IPMod.objects.raw(cmd_his)
        output = exportClassifiedXls(
            ip_allocation.columns, ip_allocation, ('alc_time','last_mod_time'), 'ip_func',
            mod_his.columns, mod_his, ('mod_time',), '操作日志',
        )
        response = FileResponse(open(output, 'rb'), as_attachment=True, filename='全量日志{}.xls'.format(timezone.now().strftime('%Y%m%d%H%M%S')))
        return response
    elif amount == 'today':
        # 当天的在网记录
        cmd_today = '''
        select a.id, a.order_num, a.client_name, a.state, a.ip, a.ip_mask, a.gateway, 
        a.bng, a.logic_port, a.svlan, a.cevlan, a.description, a.ip_func, 
        a.olt, a.service_id, a.brand_width, a.group_id, a.product_id, a.network_type, 
        a.community, a.rt, a.rd, a.comment, a.alc_user, a.alc_time, a.access_type, a.last_mod_time,
        b.identify_id, b.guard_level, b.city, b.district, b.distributor, b.distributor_contact, 
        b.demand, b.bandwidth_up, b.bandwidth_dwn, b.client_tech, b.client_tech_contact, 
        b.demand_ipv4_amount, b.demand_ipv6_amount, b.client_address, b.businessman, b.businessman_contact 
        from (
        select id, order_num, client_name, state, ip, ip_mask, gateway, 
        bng, logic_port, svlan, cevlan, description, ip_func, 
        olt, service_id, brand_width, group_id, product_id, network_type, 
        community, rt, rd, comment, alc_user, alc_time, access_type, last_mod_time , icp_id
        from MR_REC_ip_allocation
        WHERE (alc_time BETWEEN %s and %s) OR (last_mod_time BETWEEN %s and %s)) as a 
        left join MR_REC_icp_info as b
        on a.icp_id = b.id
        order by a.id desc
        '''
        timeBegin, timeEnd = getDateRange(-1)
        ip_allocation = IPAllocation.objects.raw(cmd_today, (timeBegin, timeEnd, timeBegin, timeEnd))
        # 当天的操作日志
        cmd_today_history = '''
        select a.id, a.mod_order_num, a.mod_user, a.mod_time, a.mod_type, a.mod_msg, a.order_num AS old_order_num, a.client_name as old_client_name, a.state as old_state, a.ip as old_ip, a.ip_mask as old_ip_mask,
        a.gateway as old_gateway, a.bng as old_bng, a.logic_port as old_logic_port, a.svlan as old_svlan, a.cevlan as old_cevlan, 
        a.description as old_description, a.ip_func as old_ip_func, a.olt as old_olt, a.access_type as old_access_type, a.service_id as old_service_id, a.brand_width as old_brand_width, 
        a.group_id as old_group_id, a.product_id as old_product_id, a.network_type as old_network_type, a.community as old_community, a.rt as old_rt, a.rd as old_rd,
        b.identify_id, b.guard_level, b.city, b.district, b.distributor, b.distributor_contact, 
        b.demand, b.bandwidth_up, b.bandwidth_dwn, b.client_tech, b.client_tech_contact, 
        b.demand_ipv4_amount, b.demand_ipv6_amount, b.client_address, b.businessman, b.businessman_contact 
        from (
        select id, mod_order_num, mod_user, mod_time, mod_type, mod_msg, order_num, client_name, state, ip, ip_mask,
        gateway, bng, logic_port, svlan, cevlan, 
        description, ip_func, olt, service_id, brand_width, group_id, product_id, network_type, community, rt, rd, access_type, icp_id
        from MR_REC_ip_mod_record
        where mod_time BETWEEN %s and %s) as a
        left join MR_REC_icp_info as b
        on a.icp_id = b.id
        order by a.id desc
        '''
        today_mod_history = IPAllocation.objects.raw(cmd_today_history, (timeBegin, timeEnd))
        output = exportClassifiedXls(
            ip_allocation.columns, ip_allocation, ('alc_time','last_mod_time'), 'ip_func',
            today_mod_history.columns, today_mod_history, ('mod_time',), '当天操作日志',
        )
        response = FileResponse(open(output, 'rb'), as_attachment=True, filename='当天日志{}.xls'.format(timezone.now().strftime('%Y%m%d%H%M%S')))
        return response


def allocated_client_search(request):
    context = {}
    client_search_form = ClientSearchForm(request.GET)
    if client_search_form.is_valid():
        order_num = client_search_form.cleaned_data['order_num']
        client_name = client_search_form.cleaned_data['client_name']
        group_id = client_search_form.cleaned_data['group_id']
        product_id = client_search_form.cleaned_data['product_id']
        if order_num != '':
            client_all_list = IPAllocation.objects.filter(order_num=order_num).values('order_num', 'client_name', 'group_id', 'product_id').annotate(Count('id')).order_by()
        elif client_name != '':
            client_all_list = IPAllocation.objects.filter(client_name__icontains=client_name).values('order_num', 'client_name', 'group_id', 'product_id').annotate(Count('id')).order_by()
        elif group_id is not None:
            client_all_list = IPAllocation.objects.filter(group_id=group_id).values('order_num', 'client_name', 'group_id', 'product_id').annotate(Count('id')).order_by()
        elif product_id is not None:
            client_all_list = IPAllocation.objects.filter(product_id=product_id).values('order_num', 'client_name', 'group_id', 'product_id').annotate(Count('id')).order_by()
        else:
            client_all_list = IPAllocation.objects.all().values('order_num', 'client_name', 'group_id', 'product_id').annotate(Count('id')).order_by()

    page_of_objects, page_range = pages(request, client_all_list)
    context['count'] = client_all_list.count()
    context['search_paras'] = dict2SearchParas(client_search_form.cleaned_data)
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['client_search_form'] = client_search_form
    context['new_icp_info_form'] = ICPInfoForm()
    return render(request, 'ip_allocated_client_list.html', context)


def ip_allocated_list(request):
    context = {}
    ip_all_list = IPAllocation.objects.all()
    page_of_objects, page_range = pages(request, ip_all_list)
    context['count'] = ip_all_list.count()

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['ip_search_form'] = IPAllocateSearchForm()
    return render(request, 'ip_allocated_list.html', context)


def ip_allocated_search(request):
    context = {}
    ip_search_form = IPAllocateSearchForm(request.GET)
    if ip_search_form.is_valid():
        ip_address = ip_search_form.cleaned_data['ip_address']
        order_num = ip_search_form.cleaned_data['order_num']
        client_name = ip_search_form.cleaned_data['client_name']
        group_id = ip_search_form.cleaned_data['group_id']
        product_id = ip_search_form.cleaned_data['product_id']
        community = ip_search_form.cleaned_data['community']
        if ip_address != '':
            ip_all_list = IPAllocation.objects.filter(ip=ip_address, community__icontains=community)
        elif order_num != '':
            ip_all_list = IPAllocation.objects.filter(order_num=order_num, client_name__icontains=client_name, community__icontains=community)
            if group_id is not None and product_id is not None:
                ip_all_list = IPAllocation.objects.filter(order_num=order_num, group_id=group_id, product_id=product_id, client_name__icontains=client_name, community__icontains=community)
        elif group_id is not None:
            ip_all_list = IPAllocation.objects.filter(group_id=group_id, community__icontains=community)
        elif product_id is not None:
            ip_all_list = IPAllocation.objects.filter(product_id=product_id, community__icontains=community)
        elif client_name != '':
            ip_all_list = IPAllocation.objects.filter(client_name__icontains=client_name, community__icontains=community)
        else:
            ip_all_list = IPAllocation.objects.all()
    else:
        context['ip_search_form'] = ip_search_form
        return render(request, 'ip_allocated_list.html', context)

    page_of_objects, page_range = pages(request, ip_all_list)
    context['count'] = ip_all_list.count()
    context['search_paras'] = dict2SearchParas(ip_search_form.cleaned_data)

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['ip_search_form'] = ip_search_form
    context['new_icp_info_form'] = ICPInfoForm()
    return render(request, 'ip_allocated_list.html', context)


def ajax_locate_allocated_ip(request):
    data = {}
    rid = request.GET.get('rid')
    try:
        record = IPAllocation.objects.get(id=rid)
        data = objectDataSerializer(record, data)
        if data['svlan'] is not None:
            if data['cevlan'] is not None:
                data['logic_port'] = data['logic_port']+':'+str(data['svlan'])+'.'+str(data['cevlan'])
            else:
                data['logic_port'] = data['logic_port']+':'+str(data['svlan'])+'.'+'0'
        else:
            data['logic_port'] = data['logic_port']+':'+'0.0'
        data['ip'] = '{}/{}'.format(data['ip'], data['ip_mask'])
        data['status'] = 'success'
    except ObjectDoesNotExist:
        data['status'] = 'error'
        data['error_info'] = '无法找到相应记录'
    return JsonResponse(data)

def backup_ip_allocation(old_data, mod_target, mod_order_num, mod_msg, mod_user, mod_type):
    # old_data = objectDataSerializer(mod_target, {})
    old_data['mod_target_id'] = old_data.pop('id')
    old_data.pop('comment')
    old_data.pop('alc_user')
    old_data.pop('alc_time')
    old_data.pop('last_mod_time')
    # 需要处理数据库对0时返回None的情况
    old_data['mod_order_num'] = mod_order_num
    old_data['mod_msg'] = mod_msg
    if old_data['svlan'] is None:
        old_data['svlan'] = 0
    if old_data['cevlan'] is None:
        old_data['cevlan'] = 0
    old_data['mod_user'] = mod_user
    old_data['mod_time'] = timezone.datetime.now()
    old_data['mod_type'] = mod_type
    mod_record = IPMod(**old_data)
    mod_record.save()


def ajax_mod_allocated_ip(request, operation_type):
    data = {}
    # 变更依据的校验
    if request.POST.get('mod_order_num') is None:
        data['status'] = 'error'
        data['error_info'] = '请提供有效的变更单号'
        return JsonResponse(data)
    elif request.POST.get('mod_order_num').strip() == '':
        data['status'] = 'error'
        data['error_info'] = '请提供有效的变更单号'
        return JsonResponse(data)
    else:
        mod_order_num = request.POST.get('mod_order_num').strip()
    if request.POST.get('mod_msg') is not None:
        mod_msg = request.POST.get('mod_msg').strip()
    else:
        mod_msg = ''
    if operation_type == 'mod':
        rid = request.POST.get('rid')
        form1Dict = request.POST.dict()
        if form1Dict['ip_func'] == '私网':
            form1Dict['include_private_ip'] = 'y'
        else:
            form1Dict['include_private_ip'] = 'n'
        new_ip_allocation_form = NewIPAllocationForm(form1Dict)
        form2Dict = {}
        form2Dict['ip_func'] = request.POST.get('ip_func')
        form2Dict['state'] = request.POST.get('state')
        form2Dict['first_ip'] = request.POST.get('ip')
        form2Dict['ip_num'] = 1
        form2Dict['gateway'] = request.POST.get('gateway')
        ip_target_form = IPTargetForm(form2Dict)    # form实例化可以直接传入dict
        if ip_target_form.is_valid() and new_ip_allocation_form.is_valid():
            mod_target = IPAllocation.objects.get(id=rid)
            if mod_target.state == ip_target_form.cleaned_data['state'] == "临时禁用":
                data['status'] = 'error'
                data['error_info'] = '本条记录处于禁用状态，不允许修改'
                return JsonResponse(data)
            if ip_target_form.cleaned_data['state'] == "临时禁用":
                mod_type = 'ban'    # 适配点击变更按钮来临时禁用的操作
            else:
                mod_type = 'mod'
            old_data = objectDataSerializer(mod_target, {})
            backup_ip_allocation(old_data, mod_target, mod_order_num, mod_msg, request.user.first_name, mod_type)
            # 更新新数据
            mod_target.order_num =  old_data['mod_order_num']
            mod_target.client_name = new_ip_allocation_form.cleaned_data['client_name']
            mod_target.state = ip_target_form.cleaned_data['state']
            mod_target.ip = ip_target_form.cleaned_data['first_ip'].split('/')[0]
            mod_target.ip_mask = ip_target_form.cleaned_data['first_ip'].split('/')[-1]
            mod_target.gateway = ip_target_form.cleaned_data['gateway']
            mod_target.bng = new_ip_allocation_form.cleaned_data['bng']
            mod_target.logic_port = new_ip_allocation_form.cleaned_data['logic_port']
            mod_target.svlan = new_ip_allocation_form.cleaned_data['svlan']
            mod_target.cevlan = new_ip_allocation_form.cleaned_data['cevlan']
            mod_target.description = new_ip_allocation_form.cleaned_data['description']
            mod_target.ip_func = ip_target_form.cleaned_data['ip_func']     
            mod_target.olt = new_ip_allocation_form.cleaned_data['olt']
            mod_target.service_id = new_ip_allocation_form.cleaned_data['service_id']
            mod_target.brand_width = new_ip_allocation_form.cleaned_data['brand_width']
            mod_target.group_id = new_ip_allocation_form.cleaned_data['group_id']
            mod_target.product_id = new_ip_allocation_form.cleaned_data['product_id']
            mod_target.network_type = new_ip_allocation_form.cleaned_data['network_type']
            mod_target.last_mod_time = old_data['mod_time']
            if new_ip_allocation_form.cleaned_data['include_private_ip'] == 'y':
                mod_target.community = new_ip_allocation_form.cleaned_data['community']
                mod_target.rt = new_ip_allocation_form.cleaned_data['rt']
                mod_target.rd = new_ip_allocation_form.cleaned_data['rd']
            mod_target.comment = old_data['mod_msg']
            mod_target.save()
            data['status'] = 'success'
        else:
            data['status'] = 'error'
            errorDict = ip_target_form.errors.get_json_data()
            # print(errorDict)
            for f in errorDict:
                data['error_info'] = '无效字段{}：{}'.format(f, errorDict[f][0]['message'])
            errorDict = new_ip_allocation_form.errors.get_json_data()
            # print(errorDict)
            for f in errorDict:
                data['error_info'] = '无效字段{}：{}'.format(f, errorDict[f][0]['message'])
    elif operation_type == 'ban':
        rid = request.POST.get('rid')
        mod_target = IPAllocation.objects.get(id=rid)
        if mod_target.state == "临时禁用":
            data['status'] = 'error'
            data['error_info'] = '本数据已处于禁用状态，无需再次禁用'
            return JsonResponse(data)
        old_data = objectDataSerializer(mod_target, {})
        backup_ip_allocation(old_data, mod_target, mod_order_num, mod_msg, request.user.first_name, 'ban')
        # 更新旧数据内容
        mod_target.last_mod_time = old_data['mod_time']
        mod_target.state = '临时禁用'
        mod_target.save()
        data['status'] = 'success'
    elif operation_type == 'ban_multi':
        order_num = request.POST.get('order_num')
        group_id = request.POST.get('group_id')
        product_id = request.POST.get('product_id')
        client_name = request.POST.get('client_name')
        raw_query = 'SELECT * FROM omni_agent.MR_REC_ip_allocation WHERE state != %s AND client_name LIKE %s AND group_id = %s AND order_num = %s AND product_id = %s ORDER BY alc_time DESC'
        mod_target_list = IPAllocation.objects.raw(raw_query, ('临时禁用', '%%{}%%'.format(client_name), group_id, order_num, product_id))
        # 如果不使用raw会全部实例化，导致大批量修改时溢出
        mod_time = timezone.datetime.now()
        for mod_target in mod_target_list:
            old_data = objectDataSerializerRaw(mod_target, mod_target_list.columns, {})
            backup_ip_allocation(old_data, mod_target, mod_order_num, mod_msg, request.user.first_name, 'ban')
        # update更新原分配表数据为临时禁用,已禁用的无需再禁用
        IPAllocation.objects.filter(~Q(state='临时禁用'), order_num=order_num, group_id=group_id, product_id=product_id, client_name__icontains=client_name).update(last_mod_time=mod_time, state = '临时禁用')
        data['status'] = 'success'
    elif operation_type == 'ban_multi_by_id':
        id = request.POST.get('multi_mod_target', '')
        if id == '':
            data['status'] = 'error'
            data['error_info'] = '批量操作未选定目标'
            return JsonResponse(data)
        id_list = id.split(',')
        raw_query = 'SELECT * FROM omni_agent.MR_REC_ip_allocation WHERE state != %s AND id in ({}) ORDER BY alc_time DESC'.format(','.join(['%s',]*len(id_list)))
        mod_target_list = IPAllocation.objects.raw(raw_query, ('临时禁用',)+tuple(id_list))
        mod_time = timezone.datetime.now()
        for mod_target in mod_target_list:
            old_data = objectDataSerializerRaw(mod_target, mod_target_list.columns, {})
            backup_ip_allocation(old_data, mod_target, mod_order_num, mod_msg, request.user.first_name, 'ban')
        IPAllocation.objects.filter(~Q(state='临时禁用'), id__in=tuple(id_list)).update(last_mod_time=mod_time, state = '临时禁用')
        data['status'] = 'success'
    elif operation_type == 'del': # 删除数据
        rid = request.POST.get('rid')
        mod_target = IPAllocation.objects.get(id=rid)
        old_data = objectDataSerializer(mod_target, {})
        backup_ip_allocation(old_data, mod_target, mod_order_num, mod_msg, request.user.first_name, 'del')
        mod_target.delete() # 最后删除原数据
        data['status'] = 'success'
    elif operation_type == 'del_multi': # 批量删除
        order_num = request.POST.get('order_num')
        group_id = request.POST.get('group_id')
        product_id = request.POST.get('product_id')
        client_name = request.POST.get('client_name')
        # mod_target_list = IPAllocation.objects.filter(~Q(state='临时禁用'), order_num=order_num, group_id=group_id, product_id=product_id, client_name__icontains=client_name)
        raw_query = 'SELECT * FROM omni_agent.MR_REC_ip_allocation WHERE client_name LIKE %s AND group_id = %s AND order_num = %s AND product_id = %s ORDER BY alc_time DESC'
        mod_target_list = IPAllocation.objects.raw(raw_query, ('%%{}%%'.format(client_name), group_id, order_num, product_id))
        # 如果不使用raw会全部实例化，导致大批量修改时溢出
        for mod_target in mod_target_list:
            old_data = objectDataSerializerRaw(mod_target, mod_target_list.columns, {})
            backup_ip_allocation(old_data, mod_target, mod_order_num, mod_msg, request.user.first_name, 'del')
        # delete原表数据
        IPAllocation.objects.filter(order_num=order_num, group_id=group_id, product_id=product_id, client_name__icontains=client_name).delete()
        data['status'] = 'success'
    elif operation_type == 'del_multi_by_id':
        id = request.POST.get('multi_mod_target', '')
        if id == '':
            data['status'] = 'error'
            data['error_info'] = '批量操作未选定目标'
            return JsonResponse(data)
        id_list = id.split(',')
        raw_query = 'SELECT * FROM omni_agent.MR_REC_ip_allocation WHERE id in ({}) ORDER BY alc_time DESC'.format(','.join(['%s',]*len(id_list)))
        mod_target_list = IPAllocation.objects.raw(raw_query, tuple(id_list))
        mod_time = timezone.datetime.now()
        for mod_target in mod_target_list:
            old_data = objectDataSerializerRaw(mod_target, mod_target_list.columns, {})
            backup_ip_allocation(old_data, mod_target, mod_order_num, mod_msg, request.user.first_name, 'del')
        IPAllocation.objects.filter(id__in=tuple(id_list)).delete()
        data['status'] = 'success'
    else:
        data['status'] = 'error'
        data['error_info'] = '非法操作'
    return JsonResponse(data)

def ajax_locate_icp(request):
    data = {}
    rid = request.GET.get("rid", '')
    if rid is None or rid == '' or rid == 'None':
        data['status'] = 'error'
        data['error_info'] = '此IP记录暂无ICP信息'
        return JsonResponse(data)
    try:
        record = ICP.objects.get(id=rid)
        parsed_icp_result = objectDataSerializer(record, {})
        parsed_icp_result.pop('id')
        data['parsed_icp_result'] = json.dumps(parsed_icp_result)
        data['status'] = 'success'
    except ObjectDoesNotExist:
        data['status'] = 'error'
        data['error_info'] = '无法找到相应记录'
    return JsonResponse(data)

def ajax_mod_icp_info(request, operation_type):
    data = {}
    if request.POST.get('mod_icp_order_num') is None:
        data['status'] = 'error'
        data['other_error'] = '请提供有效的变更单号'
        return JsonResponse(data)
    elif request.POST.get('mod_icp_order_num').strip() == '':
        data['status'] = 'error'
        data['other_error'] = '请提供有效的变更单号'
        return JsonResponse(data)
    else:
        mod_order_num = request.POST.get('mod_icp_order_num').strip()
    if request.POST.get('mod_icp_msg') is not None:
        mod_msg = request.POST.get('mod_icp_msg').strip()
    else:
        mod_msg = ''
    # 校验form
    new_icp_info_form = ICPInfoForm(request.POST)
    if not new_icp_info_form.is_valid():
        data['status'] = 'error'
        errorDict = new_icp_info_form.errors.get_json_data()
        data['error_info'] = json.dumps(errorDict)
        return JsonResponse(data)
    # 检查ICP记录
    try:
        # 如果存在相关记录直接使用旧记录即可
        already_has_icp = ICP.objects.get(**new_icp_info_form.cleaned_data)
    except ObjectDoesNotExist:  # 如果不存在则创建
        new_icp = ICP(**new_icp_info_form.cleaned_data)
        new_icp.save()
        already_has_icp = ICP.objects.get(**new_icp_info_form.cleaned_data)
    finally:
        if operation_type == 'mod':
            ip_record_id = request.POST.get('rid')
            new_icp_info_form = ICPInfoForm(request.POST)
            # 新增前确认是否存在一摸一样的数据
            try:
                mod_target = IPAllocation.objects.get(id=ip_record_id)
                # 如果记录和原纪录一致,则不修改
                if already_has_icp.id == mod_target.icp_id:
                    data['status'] = 'error'
                    data['other_error'] = '提供的ICP信息与原记录一致，无法变更'
                    return JsonResponse(data)
            except ObjectDoesNotExist:
                data['status'] = 'error'
                data['error_info'] = '无法找到相应记录'
                return JsonResponse(data)
            # 旧数据备份
            old_data = objectDataSerializer(mod_target, {})
            backup_ip_allocation(old_data, mod_target, mod_order_num, mod_msg, request.user.first_name, 'mod')
            # 新数据更新
            mod_target.last_mod_time = old_data['mod_time']
            mod_target.icp = already_has_icp
            mod_target.save()
            data['status'] = 'success'
        elif operation_type == 'mod_multi':
            order_num = request.POST.get('order_num_icp')
            group_id = request.POST.get('group_id_icp')
            product_id = request.POST.get('product_id_icp')
            client_name = request.POST.get('client_name_icp')
            raw_query = 'SELECT * FROM omni_agent.MR_REC_ip_allocation WHERE client_name LIKE %s AND group_id = %s AND order_num = %s AND product_id = %s ORDER BY alc_time DESC'
            mod_target_list = IPAllocation.objects.raw(raw_query, ('%%{}%%'.format(client_name), group_id, order_num, product_id))
            mod_time = timezone.datetime.now()
            for mod_target in mod_target_list:
                old_data = objectDataSerializerRaw(mod_target, mod_target_list.columns, {})
                backup_ip_allocation(old_data, mod_target, mod_order_num, mod_msg, request.user.first_name, 'mod')
            IPAllocation.objects.filter(order_num=order_num, group_id=group_id, product_id=product_id, client_name__icontains=client_name).update(last_mod_time=mod_time, icp=already_has_icp)
            data['status'] = 'success'
        else:
            data['status'] = 'error'
            data['error_info'] = '非法操作'
        return JsonResponse(data)

# 工作量统计
def list_workload(request):
    context = {}
    context['workload_search_form'] = WorkLoadSearchForm()
    return render(request, 'workload.html', context)


all_device_ip_segment_query_line = '''
    SELECT id, olt, count(DISTINCT subnet_gateway) AS gw_cnt, 
    GROUP_CONCAT(DISTINCT  CONCAT(subnet_gateway, "/", subnet_mask)) AS gws,
    cast(SUM(used_cnt) AS SIGNED) AS used, cast(SUM(all_cnt) AS SIGNED) AS total 
    FROM (
    SELECT seg_util.*, gw_olt.olt FROM (
    SELECT id, subnet_gateway, subnet_mask, SUM(if(ip_state=1, 1, 0)) AS used_cnt, COUNT(*) AS all_cnt FROM MR_REC_group_client_ip_segment 
    WHERE segment_state IS TRUE AND subnet_gateway != "" AND subnet_gateway IS NOT NULL 
    AND subnet_gateway NOT IN ( 
    SELECT gateway FROM ( 
    SELECT gateway, ip_mask, COUNT(DISTINCT olt) AS cnt 
    FROM MR_STS_ip_olt_detail 
    WHERE ip_mask != 32 
    GROUP BY gateway 
    HAVING cnt > 1 ) AS a) 
    GROUP BY subnet_gateway 
    ) AS seg_util 
    LEFT JOIN ( 
    SELECT gateway, ip_mask AS mask, olt FROM MR_STS_ip_olt_detail 
    WHERE olt LIKE "%%OLT%%" 
    GROUP BY gateway, ip_mask, olt 
    ) AS gw_olt 
    ON seg_util.subnet_gateway = gw_olt.gateway 
    HAVING olt IS NOT NULL 
    ) AS olt_util 
    GROUP BY olt 
'''

# 新增公网网段
@staff_member_required(redirect_field_name='from', login_url='login')
def list_all_ip_segment(request):
    context = {}
    all_ip_segment = GroupClientIPSegment.objects.all().values('segment', 'mask', 'segment_state').annotate(Count('ip'), used_cnt=Count('ip_state', filter=Q(ip_state__gt=0)))
    page_of_objects, page_range = pages(request, all_ip_segment)
    new_ip_segment_form = NewIpSegmentForm()
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['new_ip_segment_form'] = new_ip_segment_form
    return render(request, 'all_ip_segment.html', context)


def search_all_ip_segment(request):
    context = {}
    target_segment = request.GET.get('ip')
    all_ip_segment = GroupClientIPSegment.objects.filter(segment=target_segment).values('segment', 'mask', 'segment_state').annotate(Count('ip'), used_cnt=Count('ip_state', filter=Q(ip_state__gt=0)))
    page_of_objects, page_range = pages(request, all_ip_segment)
    new_ip_segment_form = NewIpSegmentForm()
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['new_ip_segment_form'] = new_ip_segment_form
    return render(request, 'all_ip_segment.html', context)


def ajax_confirm_new_segment(request):
    data = {}
    new_ip_segment_form = NewIpSegmentForm(request.POST)
    if new_ip_segment_form.is_valid():
        segment = new_ip_segment_form.cleaned_data['segment']
        mask = new_ip_segment_form.cleaned_data['mask']
        segment_state = new_ip_segment_form.cleaned_data['segment_state']
        snet = IP.make_net(segment, mask)
        if GroupClientIPSegment.objects.filter(segment=snet[0].strNormal()):
            data['status'] = 'error'
            data['error_info'] = '网段已存在'
        else:
            for ip in snet:
                target = GroupClientIPSegment()
                target.ip = ip.strNormal()
                target.ip_state = 0
                target.segment = snet[0].strNormal()
                target.mask = mask
                target.segment_state = segment_state
                target.save()
            data['status'] = 'success'
    else:
        data['status'] = 'error'
        data['error_info'] = '表单信息有误'
    return JsonResponse(data)

def ajax_turn_segment_state(request, operation_type):
    data = {}
    rdata = request.POST.get('rdata')
    seg, seg_mask = rdata.split('/')
    if operation_type == 'on':
        GroupClientIPSegment.objects.filter(segment=seg, mask=int(seg_mask), segment_state=False).update(segment_state=True)
        data['status'] = 'success'
        return JsonResponse(data)
    elif operation_type == 'off':
        GroupClientIPSegment.objects.filter(segment=seg, mask=int(seg_mask), segment_state=True).update(segment_state=False)
        data['status'] = 'success'
        return JsonResponse(data)
    else:
        data['status'] = 'error'
    return JsonResponse(data)

# 网段规划，需要融合上面的内容
def list_all_segment(request):
    context = {}
    all_segment = PublicIpSegment.objects.all().order_by('-id')
    page_of_objects, page_range = pages(request, all_segment)
    new_ip_segment_form = NewSchemaSegmentForm()
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['new_ip_segment_form'] = new_ip_segment_form
    return render(request, 'segment_schema.html', context)

def allocate_segment(request):
    data = {}
    new_ip_segment_form = NewSchemaSegmentForm(request.POST)
    if new_ip_segment_form.is_valid():
        segmentData = new_ip_segment_form.cleaned_data['segment']
        seg, mask = segmentData.split('/')
        specialization = new_ip_segment_form.cleaned_data['specialization']
        snet = IP.make_net(seg, mask)
        if PublicIpSegment.objects.filter(upper_segment=snet[0].strNormal()):
            data['status'] = 'error'
            data['error_info'] = '网段已存在'
        else:
            # 插入网段到mr_rec_public_segment_reference
            new_seg = PublicIpSegment()
            new_seg.upper_segment = snet[0].strNormal()
            new_seg.upper_mask = mask
            new_seg.specialization = specialization
            new_seg.save()
            for ip in snet:
                # 插入明细到mr_rec_group_client_ip_segment
                target1 = GroupClientIPSegment()
                target1.ip = ip.strNormal()
                target1.ip_state = 0
                target1.segment = snet[0].strNormal()
                target1.mask = int(mask)
                target1.segment_state = 1
                target1.save()
                # 插入明细到mr_rec_public_segment_schema
                target2 = PublicIPSegmentSchema()
                target2.ip = ip.strNormal()
                target2.upper_segment = snet[0].strNormal()
                target2.upper_mask = int(mask)
                target2.state = 0
                target2.alc_time = timezone.datetime.now()
                target2.save()
            
            data['status'] = 'success'
    else:
        data['status'] = 'error'
        data['error_info'] = '网段格式有误'
    return JsonResponse(data)

def search_segment(request):
    context = {}
    target_segment = request.GET.get('ip')
    all_segment = PublicIpSegment.objects.filter(upper_segment=target_segment).order_by('-id')
    page_of_objects, page_range = pages(request, all_segment)
    new_ip_segment_form = NewSchemaSegmentForm()
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['new_ip_segment_form'] = new_ip_segment_form
    return render(request, 'segment_schema.html', context)

def schema_detail(request):
    data = {}
    return JsonResponse(data)


# IP资源使用情况
@login_required(redirect_field_name='from', login_url='login')
@permission_required('networkresource.view_groupclientipsegment', raise_exception=True)
def get_device_allocated_segment(request):
    context = {}
    device_ip_segment_all_list = GroupClientIPSegment.objects.raw(all_device_ip_segment_query_line)
    page_of_objects, page_range = pages(request, device_ip_segment_all_list)
    expireDate, _ = getDateRange(-14)    # 系统自动清理15天前的预占，因此显示14天前的预占信息作为即将过期的信息
    almostExpireCnt = GroupClientIpReserve.objects.filter(reserved_time__lt=expireDate).values('reserved_person').annotate(Sum('reserved_cnt'))
    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['almost_expire_cnt'] = almostExpireCnt
    context['device_allocated_segment_search_form'] = DeviceIpSegmentForm()
    return render(request, 'ip_allocated_segment.html', context)


def search_device_allocated_segment(request):
    context = {}
    segment_search_form = DeviceIpSegmentForm(request.GET)
    if segment_search_form.is_valid():
        device_name = segment_search_form.cleaned_data['device_name']
        otherCmd = 'having olt like "%%{}%%"'.format(device_name)
    else:
        otherCmd = ''
    device_ip_segment_all_list = GroupClientIPSegment.objects.raw(
        all_device_ip_segment_query_line + otherCmd
    )
    page_of_objects, page_range = pages(request, device_ip_segment_all_list)
    expireDate, _ = getDateRange(-14)   # 系统自动清理15天前的预占，因此显示14天前的预占信息作为即将过期的信息
    almostExpireCnt = GroupClientIpReserve.objects.filter(reserved_time__lt=expireDate).values('reserved_person').annotate(Sum('reserved_cnt'))

    context['records'] = page_of_objects.object_list
    context['page_of_objects'] = page_of_objects
    context['page_range'] = page_range
    context['almost_expire_cnt'] = almostExpireCnt
    context['device_allocated_segment_search_form'] = segment_search_form
    context['search_paras'] = dict2SearchParas(segment_search_form.cleaned_data)
    return render(request, 'ip_allocated_segment.html', context)
    

def ajax_get_segment_used_detail(request):
    data = {}
    gws = request.GET.get('gws', '')
    gwList = [s.split('/')[0] for s in base64.b64decode(gws).decode('ascii').split(',')]
    reserved_list = GroupClientIpReserve.objects.filter(subnet_gateway__in=tuple(gwList)).order_by('-reserved_time')
    # print(reserved_list[0].reserved_person)
    reserved_dict = {}
    for r in reserved_list:
        reserved_dict[r.id] = [r.subnet_gateway+'/'+str(r.subnet_mask), r.reserved_cnt, r.reserved_person, r.contact, r.client_name, (r.reserved_time+timezone.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'), r.id]
    data['reserved_dict'] = json.dumps(reserved_dict)
    # print(data)
    data['status'] = 'success'
    return JsonResponse(data)


def ajax_get_segment_left_cnt(request):
    data = {}
    gws = request.GET.get('gws', '')
    gwList = [s.split('/')[0] for s in base64.b64decode(gws).decode('ascii').split(',')]
    # print(gwList)
    can_be_reserved_query = '''
        SELECT id, left_detail.subnet_gateway, left_detail.subnet_mask, CAST(left_detail.left_cnt-ifnull(reserve_detail.all_reserved_cnt, 0) AS SIGNED) AS can_be_reserved FROM (
        SELECT id, subnet_gateway, subnet_mask, COUNT(*) AS left_cnt FROM MR_REC_group_client_ip_segment 
        WHERE segment_state IS TRUE AND ip_state = 0 
        AND subnet_gateway IN ({}) AND subnet_gateway NOT IN ( 
        SELECT gateway FROM ( 
        SELECT gateway, ip_mask, COUNT(DISTINCT olt) AS cnt 
        FROM MR_STS_ip_olt_detail 
        WHERE ip_mask != 32 
        GROUP BY gateway 
        HAVING cnt > 1 ) AS a 
        )
        GROUP BY subnet_gateway
        ) AS left_detail
        LEFT JOIN ( 
        SELECT subnet_gateway, SUM(reserved_cnt) AS all_reserved_cnt FROM MR_REC_group_client_ip_reserve 
        WHERE subnet_gateway IN ({}) 
        GROUP BY subnet_gateway) AS reserve_detail 
        ON left_detail.subnet_gateway = reserve_detail.subnet_gateway 
    '''
    can_be_reserved_list = GroupClientIPSegment.objects.raw(
        can_be_reserved_query.format(','.join(['%s',]*len(gwList)), ','.join(['%s',]*len(gwList))),
        tuple(gwList)+tuple(gwList)
    )
    can_be_reserved_dict = {}
    for r in can_be_reserved_list:
        # can_be_reserved_dict[r.id] = r.subnet_gateway+'/'+str(r.subnet_mask)+'(剩余{}个可分配)'.format(r.can_be_reserved)
        can_be_reserved_dict[r.id] = [r.subnet_gateway, r.subnet_mask, r.can_be_reserved]
    data['can_be_reserved'] = json.dumps(can_be_reserved_dict)
    # print(data)
    data['status'] = 'success'
    return JsonResponse(data)

# IP资源预占操作
@login_required(redirect_field_name='from', login_url='login')
@permission_required('networkresource.add_groupclientipreserve', raise_exception=True)
def reserve_segment(request):
    data = {}
    reserved_gateway, reserved_mask = request.POST.get('reserved_gw').split('/')
    if request.POST.get('reserved_cnt') == '':
        data['status'] = 'error'
        data['error_info'] = '预留个数有误'
        return JsonResponse(data) 
    reserved_cnt = int(request.POST.get('reserved_cnt'))
    client_name = request.POST.get('client_name', '')
    contact = request.POST.get('contact', '')
    all_ip_left_cnt = GroupClientIPSegment.objects.filter(subnet_gateway=reserved_gateway, segment_state=1, ip_state=0).count()
    already_reserved_ip = GroupClientIpReserve.objects.filter(subnet_gateway=reserved_gateway).values('reserved_cnt')
    already_reserved_cnt = 0
    for d in already_reserved_ip:
        already_reserved_cnt += d['reserved_cnt']
    if reserved_cnt <= 0:
        data['status'] = 'error'
        data['error_info'] = '预留个数有误'
        return JsonResponse(data)
    if reserved_cnt > all_ip_left_cnt-already_reserved_cnt:
        data['status'] = 'error'
        data['error_info'] = '地址个数不足无法分配'
        return JsonResponse(data)
    if client_name == '':
        data['status'] = 'error'
        data['error_info'] = '请填写客户名'
        return JsonResponse(data)
    if contact == '' or not re.match(r'\d{11}', contact):
        data['status'] = 'error'
        data['error_info'] = '请正确填写11位的预占人联系电话'
        return JsonResponse(data)

    ip_reserve = GroupClientIpReserve()
    ip_reserve.subnet_gateway = reserved_gateway
    ip_reserve.subnet_mask = int(reserved_mask)
    ip_reserve.reserved_cnt = reserved_cnt
    ip_reserve.reserved_person = request.user.first_name
    ip_reserve.contact = contact
    ip_reserve.client_name = client_name
    ip_reserve.reserved_time = timezone.datetime.now()
    ip_reserve.save()
    data['status'] = 'success'
    return JsonResponse(data)


def cancle_reserve(request):
    data = {}
    rid = request.POST.get('rid', None)
    if rid is not None:
        try:
            record = GroupClientIpReserve.objects.get(id=rid)
            if record.reserved_person == request.user.first_name:
                record.delete()
                data['status'] = 'success'
            else:
                data['status'] = 'error'
                data['error_info'] = '越权操作：预占人与取消人账号不一致'
        except ObjectDoesNotExist:
            data['status'] = 'error'
            data['error_info'] = '记录不存在'
    else:
        data['status'] = 'error'
        data['error_info'] = '传递参数有误'

    return JsonResponse(data)


@login_required(redirect_field_name='from', login_url='login')
def ajax_get_my_reserved_list(request):
    data = {}
    reserved_person = request.user
    my_reserved_list = GroupClientIpReserve.objects.filter(reserved_person=reserved_person.first_name)
    my_reserved_dict = {}
    for my_reserved in my_reserved_list:
        my_reserved_dict[my_reserved.id] = [
            my_reserved.subnet_gateway, my_reserved.subnet_mask, my_reserved.reserved_cnt, 
            my_reserved.client_name, my_reserved.contact, 
            my_reserved.reserved_time.strftime('%Y-%m-%d'), 
        ]
    data['status'] = 'success'
    data['my_reserved_dict'] = json.dumps(my_reserved_dict)
    return JsonResponse(data)

    