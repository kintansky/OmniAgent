from django.shortcuts import render
from django.http import JsonResponse
from watchdog.models import Device
from funcpack import snmp_func
from funcpack.funcs import quickSortObj
import json
# from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
# @permission_required('watchdog.view_device', login_url='/login/')
@staff_member_required(redirect_field_name='from', login_url='login')
def link_utilization(request):
    context = {}
    return render(request, 'link_utilization.html', context)


def ajax_get_bng(request):
    data = {}
    bng = request.GET.get('bng', '')
    targets = Device.objects.filter(device_name__icontains=bng)
    if targets.count() == 0:
        data['bng_list'] = '无候选结果'
        data['status'] = 'error'
    else:
        data['bng_list'] = ','.join([t.device_name for t in targets])
        data['status'] = 'success'
    return JsonResponse(data)


def get_link_utilization(request):
    data = {}
    bngs = request.GET.get('bngs', '')
    if bngs == '' or bngs is None:
        data['status'] = 'success'
        return JsonResponse(data)
    targets = Device.objects.filter(device_name__in=bngs.split(','))
    deviceList = [(t.device_name, t.device_ip) for t in targets]
    resultData = snmp_func.mainLinkUtilization(deviceList, processNum=4)
    # 排序
    for dev in resultData:
        quickSortObj(resultData[dev], 0, len(resultData[dev])-1, 3) # sortIndex: 2->InUtilization, 3->OutUtilization
    # print(resultData)
    # ## debug
    # import time
    # time.sleep(10)
    # resultData = {}
    # resultData['GDFOS-IPMAN-BNG01-BJ-HW'] = [['OTV109_SD_BJ_BiJiangShiChang_2_H', 10, 2.34, 34, 'dT:1329-SD_BeiJiaoZhenZhengFuJieRuJiFang_OLT002_HW_MA5800:10G::10GE0/10/0']]*50
    # resultData['GDFOS-IPMAN-BNG01-DS-HW'] = [[200,]*5]*50
    # ## debug
    data['result'] = json.dumps(resultData) # 返回json数组
    data['status'] = 'success'

    return JsonResponse(data)
