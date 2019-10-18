from django.shortcuts import render
from django.http import JsonResponse
from watchdog.models import Device
# from funcpack import snmp_mp
import json

# Create your views here.
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
    # resultData = snmp_mp.main(deviceList)
    # data['result'] = json.dumps(resultData)
    # data['status'] = 'success'

    return JsonResponse(data)
